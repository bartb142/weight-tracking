from pathlib import Path
from datetime import datetime
import streamlit as st

def common_page_config():
    st.set_page_config(
        page_title='APP Name',
        layout='wide',
        page_icon='assets/small_logo.png'
    )

    LOGO_URL_LARGE = 'assets/large_logo.png'
    LOGO_URL_SMALL = 'assets/small_logo.png'
    st.logo(LOGO_URL_LARGE, link=None, icon_image=LOGO_URL_SMALL)