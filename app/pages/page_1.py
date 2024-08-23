import streamlit as st
from pymongo import MongoClient
import pandas as pd
from datetime import datetime

# Form inputs
with st.form('weight-form'):
    st.header('體重記錄表單')
    profile = st.selectbox('名字', ['Bart', 'Shelly'])
    weight = st.number_input('體重 (Kg)', min_value=None, step=0.1)
    fat_percentage = st.number_input('體脂 %', min_value=None, step=0.1)
    muscle = st.number_input('肌肉量 (Kg)', min_value=None, step=0.1)
    organ_fat_level = st.number_input('內臟脂肪(Level)', min_value=1.0, step=0.5)

    if st.form_submit_button('提交'):
        # Data to be inserted
        data = {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'profile': profile,
            'weight': weight,
            'fat_percentage': fat_percentage,
            'muscle': muscle,
            'organ_fat_level': organ_fat_level,
        }
        # MongoDB connection
        client = MongoClient('mongodb://192.168.1.5:27017/')
        db = client.weight_tracking_db
        collection = db.tracking_data

        # Insert data into MongoDB
        result = collection.insert_one(data)
        st.success('數據提交成功!')
        if result.acknowledged:
            record_id = result.inserted_id 
            record = collection.find_one({'_id':record_id})
            df = pd.DataFrame([record])
            df = df.drop(columns=['_id'])
            df = df.rename(columns={
                'date':'日期',
                'profile':'名字',
                'weight':'體重 (Kg)',
                'fat_percentage':'體脂 %',
                'muscle':'肌肉量 (Kg)',
                'organ_fat_level':'內臟脂肪(Level)'
            })
            st.dataframe(df,hide_index=True)

        client.close()