import streamlit as st
import sqlite3
import re
import json
from streamlit_extras.stylable_container import stylable_container
from streamlit_searchbox import st_searchbox
from datetime import datetime

if 'user' not in st.session_state:
    st.session_state['user'] = None
    
if 'btn_active_now' not in st.session_state:
    st.session_state['btn_active_now'] = None

# Setting up page confg
st.set_page_config(
    page_title="Dashboard Peneliti IOPRI",
    layout="wide"
)

# extract data_peneliti.json
with open("./data/data_peneliti.json", "r") as file:
    data_researcher = json.load(file)
    
    
# seach callback for search box
def search_by_regex(pattern:str) -> list[tuple[str, str]]:
    # Menggunakan list comprehension untuk mencocokkan pola regex pada key 'name'
    result = [(item['name'],item['scholar_id']) for item in data_researcher if re.search(pattern, item['name'], re.IGNORECASE)]
    
    return result 

# Retrieve data from file db
@st.cache_data()
def get_summary_data_pubs():
    sql_statement = """
        SELECT SUM(num_citations), COUNT(pub_id) FROM publications
    """
    with sqlite3.connect("data/research_ppks.db") as conn:
        cursor = conn.cursor()
        cursor.execute(sql_statement)
        result = cursor.fetchone()
        
        return {
            'num_researchers' : len(data_researcher),
            'num_papers' : result[1],
            'num_citations' : result[0],
            'citations_per_paper' : int(result[0]/result[1]),
            'citations_per_researcher' : int(result[0]/len(data_researcher))
        }
        
@st.fragment
def search_box():
    selected_box = st_searchbox(
        search_by_regex,
        key="user_searchbox",
        rerun_on_update=True,
        rerun_scope="fragment"
    )
    
    return selected_box
      
with st.sidebar:
    st.title("DASHBOARD")
    st.page_link("./views/HomePage.py", label="Home", icon="🏠")
    # st.page_link(detail_researcher, label="Detail", icon=":material/group:", type='primary', disabled=st.session_state["btn_active_now"] != )
    
    st.write("**Cari Peneliti**")
    selected_user = search_box()
    if st.button("Lihat Detail", type='primary'):
        st.session_state['user'] = selected_user
        st.switch_page("./views/Detail.py")

# style able function
def styleable_card_container(label_params:str, value_params, delta_params=None):
    with stylable_container(
        key="card_1",
        css_styles="""
            {
                border: 1px solid rgba(49, 51, 63, 0.2);
                border-radius: 0.5rem;
                padding: calc(1em - 1px);

            }
        """
    ) :
       #Content here
       st.metric(label=label_params, value=value_params, delta=delta_params)

with open("./data/data_rangkuman.json", "r") as file_summary:
    data_summary = json.load(file_summary)

with st.container():
    st.header("Informasi Paper", divider="gray")
    summary_paper = get_summary_data_pubs()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        styleable_card_container("Jumlah Peneliti", value_params=summary_paper["num_researchers"])
        styleable_card_container("Sitasi/Peniliti",value_params=summary_paper["citations_per_researcher"])
        
        
    with col2:
        styleable_card_container("Jumlah Paper", value_params=summary_paper["num_papers"])
        styleable_card_container("Sitasi/Paper",value_params=summary_paper["citations_per_paper"])

    with col3:
        styleable_card_container("Jumlah Sitasi", value_params=summary_paper["num_citations"])
        
        
# Container for list of researchers
with st.container():
    # header
    st.header("Daftar Peneliti", divider="gray")
    # st.write(data_researcher)
    
    # column for team researchers
    team_col1, team_col2, team_col3 = st.columns(3)
    
    def print_func(data):
        return data['name']
            
    with team_col1:
        
        # Gathering data
        data_pemuliaan_tanamam = [researcher for researcher in data_researcher if researcher["team"] == "Pemuliaan Tanaman"]
        
        data_bio_tekdus = [researcher for researcher in data_researcher if researcher["team"] == "Bioteknologi & Bioindustri"]
        
        # Method for handling onchange selectbox
        
        def switch_page_pemuliaan():
            if st.session_state['pemuliaan_selected'] is None:
                if st.session_state["btn_active_now"] is not None and st.session_state["btn_active_now"] == "pemuliaan":
                    st.session_state["btn_active_now"] = None 
                pass
            else:
                selected_user = st.session_state['pemuliaan_selected']
                st.session_state['user'] = selected_user["scholar_id"]
                st.session_state["btn_active_now"] = "pemuliaan"
                
        def switch_page_biotekdus():
            if st.session_state['biotekdus_selected'] is None:
                if st.session_state["btn_active_now"] is not None and st.session_state["btn_active_now"] == "biotekdus":
                    st.session_state["btn_active_now"] = None 
                pass
            else:
                selected_user = st.session_state['biotekdus_selected']
                st.session_state['user'] = selected_user["scholar_id"]
                st.session_state["btn_active_now"] = "biotekdus"
        
        # Displaying Data
        title_button_pemuliaan = st.columns([0.8, 0.2])
        
        with title_button_pemuliaan[0]:
            st.write("**Pemuliaan Tanaman**")
        with title_button_pemuliaan[1]:
            if st.button(label="", key="btn_cari_pemuliaan", icon=":material/search:", type='primary', disabled=st.session_state["btn_active_now"] != "pemuliaan"):
                st.switch_page("./views/Detail.py")
        
        st.selectbox(
            label="**Pemuliaan Tanaman**",
            options=data_pemuliaan_tanamam,
            index=None,
            label_visibility="collapsed",
            format_func=print_func,
            key="pemuliaan_selected",
            on_change=switch_page_pemuliaan
        )
        
        title_button_biotekdus = st.columns([0.8, 0.2])
        
        with title_button_biotekdus[0]:
            st.write("**Bioteknologi & Bioindustri**")
        with title_button_biotekdus[1]:
            if st.button(label="", key="btn_cari_biotekdus", icon=":material/search:", type='primary', disabled=st.session_state["btn_active_now"] != "biotekdus"):
                st.switch_page("./views/Detail.py")
        
        st.selectbox(
            label="**Bioteknologi & Bioindustri**",
            options=data_pemuliaan_tanamam,
            index=None,
            label_visibility="collapsed",
            format_func=print_func,
            key="biotekdus_selected",
            on_change=switch_page_biotekdus
        )
        
    with team_col2:
        # Gathering data
        data_tanah_agro = [researcher for researcher in data_researcher if researcher["team"] == "Ilmu Tanah dan Agronomi"]
        
        data_hilirisasi = [researcher for researcher in data_researcher if researcher["team"] == "Hilirisasi"]
        
        # Method to handle onchange selectbox
        def switch_page_agronomi():
            if st.session_state['agronomi_selected'] is None:
                if st.session_state["btn_active_now"] is not None and st.session_state["btn_active_now"] == "agronomi":
                    st.session_state["btn_active_now"] = None 
                pass
            else:
                selected_user = st.session_state['agronomi_selected']
                st.session_state['user'] = selected_user["scholar_id"]
                st.session_state["btn_active_now"] = "agronomi"
                
        def switch_page_hilirisasi():
            if st.session_state['hilirisasi_selected'] is None:
                if st.session_state["btn_active_now"] is not None and st.session_state["btn_active_now"] == "hilirisasi":
                    st.session_state["btn_active_now"] = None 
                pass
            else:
                selected_user = st.session_state['hilirisasi_selected']
                st.session_state['user'] = selected_user["scholar_id"]
                st.session_state["btn_active_now"] = "hilirisasi"
        
        
        # Displayin data
        title_button_agronomi = st.columns([0.8, 0.2])
        
        with title_button_agronomi[0]:
            st.write("**Ilmu Tanah dan Agronomi**")
        with title_button_agronomi[1]:
            if st.button(label="", key="btn_cari_agronomi", icon=":material/search:", type='primary', disabled=st.session_state["btn_active_now"] != "agronomi"):
                st.switch_page("./views/Detail.py")
            
        st.selectbox(
            label="**Ilmu Tanah dan Agronomi**",
            options=data_tanah_agro,
            index=None,
            label_visibility="collapsed",
            format_func=print_func,
            key="agronomi_selected",
            on_change=switch_page_agronomi
        )
        
        title_button_hilirisasi = st.columns([0.8, 0.2])
        
        with title_button_hilirisasi[0]:
            st.write("**Hilirisasi**")
        with title_button_hilirisasi[1]:
            if st.button(label="", key="btn_cari_hilirisasi", icon=":material/search:", type='primary', disabled=st.session_state["btn_active_now"] != "hilirisasi"):
                st.switch_page("./views/Detail.py")
            
        st.selectbox(
            label="**Hilirisasi**",
            options=data_hilirisasi,
            index=None,
            label_visibility="collapsed",
            format_func=print_func,
            key="hilirisasi_selected",
            on_change=switch_page_hilirisasi
        )
        
    with team_col3:
        # Gathering Data
        data_proteksi_tanaman = [researcher for researcher in data_researcher if researcher["team"] == "Proteksi Tanaman"]
        
        data_sosio_ekoling = [researcher for researcher in data_researcher if researcher["team"] == "Sosio Tekno Ekonomi & Lingkungan"]
        
        # Method to handle on change value selectbox
        def switch_page_proteksi():
            if st.session_state['proteksi_selected'] is None:
                if st.session_state["btn_active_now"] is not None and st.session_state["btn_active_now"] == "proteksi":
                    st.session_state["btn_active_now"] = None 
                pass
            else:
                selected_user = st.session_state['proteksi_selected']
                st.session_state['user'] = selected_user["scholar_id"]
                st.session_state["btn_active_now"] = "proteksi"
                
        def switch_page_sosio():
            if st.session_state['sosio_selected'] is None:
                if st.session_state["btn_active_now"] is not None and st.session_state["btn_active_now"] == "sosio":
                    st.session_state["btn_active_now"] = None 
                pass
            else:
                selected_user = st.session_state['sosio_selected']
                st.session_state['user'] = selected_user["scholar_id"]
                st.session_state["btn_active_now"] = "sosio"
        
        
        # Displaying for data porteksi tanaman
        title_button_agronomi = st.columns([0.8, 0.2])
        
        with title_button_agronomi[0]:
            st.write("**Proteksi Tanaman**")
        with title_button_agronomi[1]:
            if st.button(label="", key="btn_cari_proteksi", icon=":material/search:", type='primary', disabled=st.session_state["btn_active_now"] != "proteksi"):
                st.switch_page("./views/Detail.py")
        
    
        st.selectbox(
            label="**Ilmu Tanah dan Agronomi**",
            options=data_proteksi_tanaman,
            index=None,
            label_visibility="collapsed",
            format_func=print_func,
            key="proteksi_selected",
            on_change=switch_page_proteksi
        )


        # Displaying for data porteksi tanaman
        title_button_agronomi = st.columns([0.8, 0.2])
        
        with title_button_agronomi[0]:
            st.write("**Sosio Tekno Ekonomi & Lingkungan**")
        with title_button_agronomi[1]:
            if st.button(label="", key="btn_cari_sosio", icon=":material/search:", type='primary', disabled=st.session_state["btn_active_now"] != "sosio"):
                st.switch_page("./views/Detail.py")
        
            
        st.selectbox(
            label="**Sosio Tekno Ekonomi & Lingkungan**",
            options=data_sosio_ekoling,
            index=None,
            label_visibility="collapsed",
            format_func=print_func,
            key="sosio_selected",
            on_change=switch_page_sosio
        )
