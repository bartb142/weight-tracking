import streamlit as st
from pymongo import MongoClient
import pandas as pd
import plotly.express as px

# MongoDB connection
client = MongoClient("mongodb://192.168.1.5:27017/")
db = client.weight_tracking_db
collection = db.tracking_data

# Display existing data as a DataFrame
st.header("數據看板")
data_records = list(collection.find())

if data_records:
    df = pd.DataFrame(data_records)
    df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
    df = df.drop(columns=["_id"])  # Drop the MongoDB _id column if not needed
    data_exist = True
else:
    st.write("No data recorded yet.")
    data_exist = False

client.close()

if data_exist:
    st.dataframe(df,hide_index=True)
    profile_picker = st.multiselect(
        label='Year filter:',
        options=df['profile'].unique(),
        default=['Bart','Shelly']
    )

    if 'Bart' in profile_picker:
        # Bart
        st.header('Bart')
        bart_df = df.query('profile == "Bart"')
        bart_df = bart_df.drop(columns='profile')
        bart_df = bart_df.sort_values(by='date', ascending=False)
        l7_bart_avgs = bart_df.head(7).drop(columns='date').mean()
        # Metrics
        col1, col2, col3 = st.columns(3)
        col1.metric('最近七次平均體重(Kg)',l7_bart_avgs['weight'])
        col2.metric('最近七次平均肌肉量 (Kg)',l7_bart_avgs['muscle'])
        col3.metric('最近七次平均體脂率(%)',l7_bart_avgs['fat_percentage'])
        # Charts Config
        bart_weight_fig = px.scatter(bart_df, x='date', y=['weight','muscle']).update_layout(
            xaxis_title='日期', 
            yaxis_title='體重(Kg)',
            xaxis=dict(
                tickformat="%Y-%m-%d",  # Date format (Year-Month-Day)
                dtick="D1")
            )
        bart_weight_fig.for_each_trace(lambda trace: trace.update(name={
            'weight': '體重 (Kg)',
            'muscle': '肌肉量 (Kg)'
        }.get(trace.name, trace.name)))

        bart_fat_fig = px.scatter(bart_df, x='date', y=['fat_percentage','organ_fat_level']).update_layout(
            xaxis_title='日期', 
            yaxis_title='體脂率％/內臟脂肪 Level',
            xaxis=dict(
                tickformat="%Y-%m-%d",  # Date format (Year-Month-Day)
                dtick="D1"))
        bart_fat_fig.for_each_trace(lambda trace: trace.update(name={
            'fat_percentage':'體脂 %',
            'organ_fat_level':'內臟脂肪(Level)'
        }.get(trace.name, trace.name)))
        # Chart Display
        st.plotly_chart(bart_weight_fig, theme='streamlit', on_select='rerun', selection_mode='points')
        st.plotly_chart(bart_fat_fig, theme='streamlit', on_select='rerun', selection_mode='points')

    if 'Shelly' in profile_picker:    
        # Shelly 
        st.header('Shelly')
        shelly_df = df.query('profile == "Shelly"')
        shelly_df = shelly_df.drop(columns='profile')
        shelly_df = shelly_df.sort_values(by='date', ascending=False)
        l7_shelly_avgs = shelly_df.head(7).drop(columns='date').mean()
        # Metrics
        col1, col2, col3 = st.columns(3)
        col1.metric('最近七次平均體重(Kg)',l7_shelly_avgs['weight'])
        col2.metric('最近七次平均肌肉量 (Kg)',l7_shelly_avgs['muscle'])
        col3.metric('最近七次平均體脂率(%)',l7_shelly_avgs['fat_percentage'])
        # Charts Config
        shelly_weight_fig = px.scatter(shelly_df, x='date', y=['weight','muscle']).update_layout(
            xaxis_title='日期', 
            yaxis_title='體重(Kg)',
            xaxis=dict(
                tickformat="%Y-%m-%d",  # Date format (Year-Month-Day)
                dtick="D1"))
        shelly_weight_fig.for_each_trace(lambda trace: trace.update(name={
            'weight': '體重 (Kg)',
            'muscle': '肌肉量 (Kg)'
        }.get(trace.name, trace.name)))

        shelly_fat_fig = px.scatter(shelly_df, x='date', y=['fat_percentage','organ_fat_level']).update_layout(
            xaxis_title='日期', 
            yaxis_title='體脂率％/內臟脂肪 Level',
            xaxis=dict(
                tickformat="%Y-%m-%d",  # Date format (Year-Month-Day)
                dtick="D1"))
        shelly_fat_fig.for_each_trace(lambda trace: trace.update(name={
            'fat_percentage':'體脂 %',
            'organ_fat_level':'內臟脂肪(Level)'
        }.get(trace.name, trace.name)))

        # Chart Display
        st.plotly_chart(shelly_weight_fig, theme='streamlit', on_select='rerun', selection_mode='points')
        st.plotly_chart(shelly_fat_fig, theme='streamlit', on_select='rerun', selection_mode='points')
