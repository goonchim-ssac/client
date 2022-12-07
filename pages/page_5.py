import streamlit as st
import requests
import pandas as pd

URL = "http://127.0.0.1:9000/item/"

st.title('🔍 상품 조회')

product = st.text_input("조회할 상품의 바코드를 입력해주세요.")

if st.button('조회'):
    if product == None:
        res = requests.get(url=URL) # 전체 조회
        print(res.json())
        if len(res.json()) == 0:
            st.write("등록된 상품이 없습니다.")
        else:
            df = pd.DataFrame.from_records(res.json())
            df = df[['item_cd', 'item_nm', 'item_cat_nm', 'item_maker']]
            df.rename(columns={'item_cd':'바코드', 'item_nm':'상품명', 'item_cat_nm':'상품 분류', 'item_maker':'제조사'}, inplace=True)
            st.dataframe(df)
    else:
        res = requests.get(url=URL, json={"item_cd" : product})
        df = pd.DataFrame.from_records(res.json())
        df = df[['item_cd', 'item_nm', 'item_cat_nm', 'item_maker']]
        df.rename(columns={'item_cd':'바코드', 'item_nm':'상품명', 'item_cat_nm':'상품 분류', 'item_maker':'제조사'}, inplace=True)
        st.dataframe(df)
