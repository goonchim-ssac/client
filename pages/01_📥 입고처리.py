import streamlit as st

import streamlit as st
from webcam import webcam # pip install streamlit-webcam-example
import pyautogui
import requests
from PIL import Image
from post_processing import text_postprocessing
import time

st.title('📥 입고처리')

barcode = st.text_input('빈 칸에 바코드를 입력해주세요.', placeholder='13자리를 입력해주세요', max_chars=13)

        
if len(barcode) == 13:
    #st.success(f' < 바코드번호 : {barcode} / {count} 개 > ')
    #st.write(f'입력된 바코드는 <{barcode}> 입니다.')
    # Create Radio Buttons
    check_cam = st.radio(label = '< 내장캠 / 웹캠 > 을 선택해주세요.', options = ['Maincam', 'Webcam'])
    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
        
    if check_cam == 'Maincam': # 내장 캠인 경우
        captured_image = st.camera_input('상품의 유통기한을 인식해주세요.') # type : <class 'streamlit.runtime.uploaded_file_manager.UploadedFile'>
        
        if captured_image is None:
            st.write('정면으로 인식되었다면 <Take Photo> 를 눌러주세요.')
            
        else:
            #st.image(captured_image)
            captured_image = Image.open(captured_image) # image mode 기본 값이 rgb이므로 그대로 사용
            captured_image.save('image.jpg')
            image = open('image.jpg', 'rb') # retval: <_io.BufferedReader name='image.jpg'> (buffered I/O (바이너리 스트림))
            
            upload = {'file': image}
            res = requests.post(url='http://127.0.0.1:8000/exp_date', files=upload)
            
            st.write(f'< 바코드번호 : {barcode}>')
            st.write('상품정보 : 사람')
            st.write('유통기한 : 2100년')
            st.write('삐-빅 정상입니다')
            st.write('-------')
            
            check_info = st.radio(label = '유통기한 정보를 확인해주세요.', options = ['확인', '직접입력'])
            
            if check_info == '확인': # 내장 캠인 경우
                count = st.number_input('수량을 입력해주세요.', 0, 1000)
                #st.button('등록')
        
                if "button_clicked" not in st.session_state:
                    st.session_state.button_clicked = False
                    
                def callback():
                    st.session_state.button_clicked = True
                        
                if (st.button("등록", on_click = callback
                                    or st.session_state.button_clicked)):
                    st.success(f' < 바코드번호 : {barcode} / {count} 개 > 등록되었습니다.')
                    
            
            else :
                ex1, co2 = st.columns(2)
                
                with ex1 :
                    #exdate = st.date_input('유통기한을 입력해주세요.', placeholder='YYYY MM DD', max_chars=8)
                    exdate = st.date_input('유통기한을 입력해주세요.')
                
                with co2 :
                    count = st.number_input('수량을 입력해주세요', 0, 1000)
                #st.button('등록')
        
                if "button_clicked" not in st.session_state:
                    st.session_state.button_clicked = False
                    
                def callback():
                    st.session_state.button_clicked = True
                        
                if (st.button("등록", on_click = callback
                                    or st.session_state.button_clicked)):
                    st.success(f' < 바코드번호 : {barcode} / {count} 개 > 등록되었습니다 ')
                                    
            

                
    else: # 외장 캠인 경우
        captured_image = st.camera_input('상품의 유통기한을 인식해주세요') # type : <class 'streamlit.runtime.uploaded_file_manager.UploadedFile'>
        
        if captured_image is None:
            st.write('정면으로 인식되었다면 <Take Photo> 를 눌러주세요')
            
        else:
            #st.image(captured_image)
            captured_image = Image.open(captured_image) # image mode 기본 값이 rgb이므로 그대로 사용
            captured_image.save('image.jpg')
            image = open('image.jpg', 'rb') # retval: <_io.BufferedReader name='image.jpg'> (buffered I/O (바이너리 스트림))
            
            upload = {'file': image}
            res = requests.post(url='http://127.0.0.1:8000/exp_date', files=upload)
            
            st.write(f'< 바코드번호 : {barcode}>')
            st.write('상품정보 : 사람')
            st.write('유통기한 : 2100년')
            st.write('삐-빅 정상입니다')
            st.write('-------')

            
            check_info = st.radio(label = '유통기한 정보를 확인해주세요', options = ['확인', '직접입력'])
            
            if check_info == '확인': # 내장 캠인 경우
                count = st.number_input('수량을 입력해주세요', 0, 1000)
                #st.button('등록')
        
                if "button_clicked" not in st.session_state:
                    st.session_state.button_clicked = False
                    
                def callback():
                    st.session_state.button_clicked = True
                        
                if (st.button("등록", on_click = callback
                                    or st.session_state.button_clicked)):
                    st.success(f' < 바코드번호 : {barcode} / {count} 개 > 등록되었습니다 ')
                    
            
            else :
                ex1, co2 = st.columns(2)
                
                with ex1 :
                    #exdate = st.date_input('유통기한을 입력해주세요.', placeholder='YYYY MM DD', max_chars=8)
                    exdate = st.date_input('유통기한을 입력해주세요.')
                
                with co2 :
                    count = st.number_input('수량을 입력해주세요', 0, 1000)
                #st.button('등록')
        
                if "button_clicked" not in st.session_state:
                    st.session_state.button_clicked = False
                    
                def callback():
                    st.session_state.button_clicked = True
                        
                if (st.button("등록", on_click = callback
                                    or st.session_state.button_clicked)):
                    st.success(f' < 바코드번호 : {barcode} / {count} 개 > 등록되었습니다 ')
                    
elif 0 < len(barcode) < 13 or 13 < len(barcode):
        st.error('바코드를 다시 입력해주세요.')