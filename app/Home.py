import streamlit as st
from pymongo import MongoClient
import pandas as pd
from datetime import datetime


st.set_page_config(
    page_title='Weight Tracker',
    layout='wide',
    page_icon='assets/small_logo.png'
)

LOGO_URL_LARGE = 'assets/large_logo.png'
LOGO_URL_SMALL = 'assets/small_logo.png'
st.logo(LOGO_URL_LARGE, link=None, icon_image=LOGO_URL_SMALL)

# Page setup 
page1 = st.Page(
    page='pages/page_1.py',
    title='體重記錄',
    icon=':material/add_notes:',
    default=True,
)

page2 = st.Page(
    page='pages/page_2.py',
    title='數據看板',
    icon=':material/bar_chart:',
)

page3 = st.Page(
    page='pages/page_3.py',
    title='數據分析工具',
    icon=':material/analytics:',
)

# Nav setup
pg = st.navigation(pages=[page1,page2,page3])
pg .run()