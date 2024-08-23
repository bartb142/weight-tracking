import streamlit as st
from pymongo import MongoClient
import pandas as pd

# MongoDB connection
client = MongoClient("mongodb://192.168.1.5:27017/")
db = client.weight_tracking_db
collection = db.tracking_data

# Display existing data as a DataFrame
st.header("數據看板")
data_records = list(collection.find())

if data_records:
    df = pd.DataFrame(data_records)
    df = df.drop(columns=["_id"])  # Drop the MongoDB _id column if not needed
    st.dataframe(df,hide_index=True)
else:
    st.write("No data recorded yet.")

client.close()