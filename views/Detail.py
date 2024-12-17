import streamlit as st
import plotly.express as px
import pandas as pd
import json
import re
from scholarly import scholarly
from streamlit_extras.stylable_container import stylable_container
from streamlit_searchbox import st_searchbox
# st.rerun()

if 'user' not in st.session_state:
    st.session_state['user'] = None

if 'btn_active_now' in st.session_state:
    st.session_state['btn_active_now'] = None
    
# Setting up page confg
st.set_page_config(
    page_title="Dashboard Peneliti IOPRI",
    layout="wide"
)

# Get Data
@st.cache_data()
def get_author_info(author_id:str):
    # Get Author Informatin from Google Scholar
    author_info = scholarly.search_author_id(author_id)
    
    # Get further information about author
    author_info = scholarly.fill(author_info, sections=["basics", "indices", "counts", "publications"])
    
    return author_info

def extract_basic_info_author(author_info_params):
    # Get Information
    profile = {
      'name': author_info_params['name'],
      'affiliation': author_info_params['affiliation'],
      'interests': author_info_params['interests'],
      'url_picture': author_info_params['url_picture'] if 'url_picture' in author_info_params else "assets/avatar.png"
    }
    
    return profile

def extract_graph_cited_info_author(author_info_params):
    data_graph = []
    
    for year, cites in author_info_params['cites_per_year'].items():
        data_graph.append({
            'year' : year,
            'cites' : cites,
        })
        
    return data_graph

def extrac_pubs_info_author(author_info_params):
    # extracting publications data
    publications = []
    for publication in author_info_params['publications']:
        # Membuat dictionary baru untuk menyimpan data yang diinginkan
        pub_info = {
            'title': publication['bib'].get('title', ''),
            'pub_year': publication['bib'].get('pub_year', ''),
            'citation': publication['bib'].get('citation', ''),
            'author': publication['bib'].get('author', ''),
            'num_citations': publication['num_citations']
        }
        # Menambahkan dictionary ke list
        publications.append(pub_info)

    # konversi list dict ke dataframe
    df_publications = pd.DataFrame(publications)
    return df_publications

def border_rad_photo_frame(image_src):
    with stylable_container(
        key="frame_photo",
        css_styles="""
            img {
                aspect-ratio: 1 / 1;
                width: 100%;
                height: auto;
                object-fit: cover;
                border-radius: 50%
            }
        """
    ):
        st.image(image_src, use_column_width=True)
        
@st.fragment
def search_box():
    selected_box = st_searchbox(
        search_by_regex,
        key="user_searchbox",
        rerun_on_update=True,
        rerun_scope="fragment"
    )
    
    return selected_box
            
        
# extract data_peneliti.json
with open("./data/data_peneliti.json", "r") as file:
    data_researcher = json.load(file)
    
    
# seach callback for search box
def search_by_regex(pattern:str) -> list[tuple[str, str]]:
    # Menggunakan list comprehension untuk mencocokkan pola regex pada key 'name'
    result = [(item['name'],item['scholar_id']) for item in data_researcher if re.search(pattern, item['name'], re.IGNORECASE)]
    
    return result   
    
with st.sidebar:
    st.title("DASHBOARD")
    st.page_link("./views/HomePage.py", label="Home", icon="🏠")
    # st.page_link(detail_researcher, label="Detail", icon=":material/group:")
    
    st.write("**Cari Peneliti**")
    user_selected = search_box()
    if st.button("Lihat Detail", type='primary'):
        st.session_state['user'] = user_selected
    
try:
    author_id = st.session_state['user']
except Exception as e:
    st.error("**404: Page not found**")
    st.error("The page you are looking for does not exist.")
    st.stop()

# Get Data for Profile Author
try:
    author_info = get_author_info(author_id=author_id)
except:
    st.warning("⚠ Author Tidak Ditemukan")
    st.stop()
    
basic_author_info = extract_basic_info_author(author_info)
graph_cited_data = extract_graph_cited_info_author(author_info)
df_publications = extrac_pubs_info_author(author_info)


user_detail_info, cited_info = st.columns([0.7, 0.3], gap='medium')


with stylable_container(
    key="container_detail",
    css_styles="""
        div {
            border-right: 5px solid red;
        }
    """
):
    with user_detail_info:
        profile_img, profile_detail = st.columns([0.2, 0.8])
        with profile_img:
            border_rad_photo_frame(basic_author_info["url_picture"])
        
        with profile_detail:
            st.subheader(basic_author_info["name"])
            st.write(basic_author_info["affiliation"])
            st.write(", ".join(basic_author_info["interests"]))
            
            
        # Publication Info
        pub_info_to_display = df_publications[["title", "pub_year", "num_citations"]]
        
        st.dataframe(pub_info_to_display, hide_index=True, column_config={
            "title" : "Judul",
            "pub_year" : "Tahun",
            "num_citations": "Jumlah Sitasi"
        }, use_container_width=True)    
        
with cited_info:
    st.subheader("Informasi Kutipan", divider=True)
    
    
    # Information summary for autho;
    # Not finished yet 
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Kutipan", 200, delta=None, delta_color="normal", help=None, label_visibility="visible")
        st.metric("Total Kutipan", 200, delta=None, delta_color="normal", help=None, label_visibility="visible")

    with col2:
        st.metric("Total Kutipan", 200, delta=None, delta_color="normal", help=None, label_visibility="visible")
        st.metric("Total Kutipan", 200, delta=None, delta_color="normal", help=None, label_visibility="visible")
        
    st.divider()

    df_data_cited = pd.DataFrame(graph_cited_data)
    st.bar_chart(df_data_cited, x="year", y="cites", x_label="Tahun", y_label="Jumlah")
