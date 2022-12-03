from datetime import datetime
import streamlit as st
import requests

url = "http://52.78.154.186:9000/stock/"

st.title('🔍 입고조회')

col1, col2 = st.columns(2)


with col1:
    front_time = st.date_input("조회 시작 기간", datetime.today())
    front_time = str(front_time).replace("-", "/")
    st.write(front_time)
with col2:
    back_time = st.date_input("조회 종료 기간", datetime.today())
    back_time = str(back_time).replace("-", "/")
    st.write(back_time)
    
if front_time != None and back_time != None:
    res = requests.get(url, params = {"period_front":front_time, "period_back":back_time})

st.write(res.json())