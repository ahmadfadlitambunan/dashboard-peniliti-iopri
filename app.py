import streamlit as st
from streamlit_searchbox import st_searchbox
import os

# st.write(os.getcwd())
# --- Page Setup ---
home_page = st.Page(
    page="./views/HomePage.py",
    title="Home",
    icon=":material/home:",
    default=True
)

detail_researcher = st.Page(
    page="./views/Detail.py",
    title="Peneliti",
    icon=":material/group:",
    url_path="detail"
)

# --- Navigation Setup ---
pg = st.navigation(
    {
        "DASHBOARD" : [home_page, detail_researcher]
    },
    position="hidden"
)


# --- Navigation Run ---
pg.run()
        