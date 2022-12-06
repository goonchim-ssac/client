import streamlit as st

qrcode = st.text_input('상품의 QR을 입력해주세요.', max_chars=21)
qr_bc = qrcode[0:12]
qr_ex = (f'{qrcode[13:17]}/{qrcode[17:19]}/{qrcode[19:21]}')

if len(qrcode) == 21:
    st.write(f'해당 상품의 바코드는 {qr_bc}, 유통기한은 {qr_ex} 입니다.')
    st.write('상품정보 : api 연결')
    st.button('출고')
    