from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parent.parent))

import streamlit as st
from webcam import webcam
from datetime import datetime
import requests
import re

from component.config import DB_SERVER_URL, INFERENCE_SERVER_URL, STOCK
from component.func import ImageFile
from component.post_processing import get_expdate


# 기본 설정
if 'last' not in st.session_state:
    st.session_state.last = None

if "button_clicked" not in st.session_state:
    st.session_state.button_clicked = False
                    
def button_clicked():
    st.session_state.button_clicked = True


st.title('📥 입고처리')

barcode = st.text_input('빈 칸에 바코드를 입력해주세요.', placeholder='13자리를 입력해주세요', max_chars=13)

        
if len(barcode) == 13:
    check_cam = st.radio(label = '< 내장캠 / 웹캠 > 을 선택해주세요.', options = ['Maincam', 'Webcam'])
    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
        
    if check_cam == 'Maincam': # 내장 캠인 경우

        image_file = ImageFile()
        captured_image = st.camera_input('상품의 유통기한을 인식해주세요.')

        if captured_image is None:
            st.write('정면으로 인식되었다면 <Take Photo> 를 눌러주세요.')
            
        else:
            buffered_stream = image_file.image_to_buffer(captured_image)
            upload = {'file': buffered_stream}

            # 추론
            inference = requests.post(url="http://127.0.0.1:8000/exp_date", files=upload)
            exp_date = get_expdate(inference.json()["exp_date"])

            # 화면에 표시할 정보
            st.write(f'< 바코드번호 : {barcode}>')
            st.write('상품정보 : 사람')
            st.write(f'유통기한 : {exp_date}')
            st.write('삐-빅 정상입니다')
            st.write('-------')

            # 재촬영인 경우 재학습용 DB 서버로 보냄
            if st.session_state.last != None:
                buffered_stream = image_file.image_to_buffer(captured_image)
                upload = {'file': buffered_stream}
                res = requests.post(url=DB_SERVER_URL, files=upload)
                print("재촬영 이미지 DB 전송 결과 :", res)
            st.session_state.last = buffered_stream # 다음 촬영 시 보내기 위해 저장
            image_file.drop_image(buffered_stream) # 이미지 파일 삭제
            

            # 예측된 유통기한을 그대로 사용할지(확인), 수정하여 사용할지(직접입력) 선택
            check_info = st.radio(label = '유통기한 정보를 확인해주세요.', options = ['확인', '직접입력'])     
            
            # 확인
            if check_info == '확인':
                count = st.number_input('수량을 입력해주세요.', 0, 1000)
                st.button("등록", on_click = button_clicked)
                if st.session_state.button_clicked:
                    st.success(f' < 바코드번호 : {barcode} / {count} 개 > 등록되었습니다.')
            
            # 직접 입력
            else :
                ex1, co2 = st.columns(2)
                with ex1 :
                    exdate = st.date_input('유통기한을 입력해주세요.')
                with co2 :
                    count = st.number_input('수량을 입력해주세요', 0, 1000)
                st.button("등록", on_click = button_clicked)
                        
                if st.session_state.button_clicked:
                    st.success(f' < 바코드번호 : {barcode} / {count} 개 > 등록되었습니다 ')
            

            ls_dt = str(datetime.today())
            ls_dt = re.sub('[.|:]', '', ls_dt)

            data = {
                'ls_dt': ls_dt,
                'barcode': barcode,
                'ex_dt': exp_date,
                'ls_ct': count
                }
            res = requests.post(url=STOCK, data=data)

    # 외장 캠인 경우           
    else:
        image_file = ImageFile()
        captured_image = webcam('상품의 유통기한을 인식해주세요')
        
        if captured_image is None:
            st.write('정면으로 인식되었다면 <Take Photo> 를 눌러주세요')
            
        else:
            buffered_stream = image_file.image_to_buffer(captured_image)
            upload = {'file': buffered_stream}

            # 추론
            inference = requests.post(url="http://127.0.0.1:8000/exp_date", files=upload)
            print(inference.text)
            exp_date = get_expdate(inference.json()["exp_date"])

            # 화면에 표시할 정보
            st.write(f'< 바코드번호 : {barcode}>')
            st.write('상품정보 : 사람')
            st.write(f'유통기한 : {exp_date}')
            st.write('삐-빅 정상입니다')
            st.write('-------')

            # 재촬영인 경우 재학습용 DB 서버로 보냄
            if st.session_state.last != None:
                buffered_stream = image_file.image_to_buffer(captured_image)
                upload = {'file': buffered_stream}
                res = requests.post(url=DB_SERVER_URL, files=upload)
                print("재촬영 이미지 DB 전송 결과 :", res)
            
            st.session_state.last = buffered_stream # 다음 촬영 시 보내기 위해 저장
            image_file.drop_image(buffered_stream) # 이미지 파일 삭제


            # 예측된 유통기한을 그대로 사용할지(확인), 수정하여 사용할지(직접입력) 선택
            check_info = st.radio(label = '유통기한 정보를 확인해주세요', options = ['확인', '직접입력'])
            
            # 확인
            if check_info == '확인':
                count = st.number_input('수량을 입력해주세요', 0, 1000)
                st.button("등록", on_click = button_clicked)
                        
                if st.session_state.button_clicked:
                    st.success(f' < 바코드번호 : {barcode} / {count} 개 > 등록되었습니다 ')
                    
            # 직접 입력
            else :
                ex1, co2 = st.columns(2)
                with ex1 :
                    exdate = st.date_input('유통기한을 입력해주세요.')
                with co2 :
                    count = st.number_input('수량을 입력해주세요', 0, 1000)
                st.button("등록", on_click = button_clicked)
                        
                if st.session_state.button_clicked:
                    st.success(f' < 바코드번호 : {barcode} / {count} 개 > 등록되었습니다 ')
                    

            ls_dt = str(datetime.today())
            ls_dt = re.sub('[.|:]', '', ls_dt)

            data = {
                'ls_dt': ls_dt,
                'barcode': barcode,
                'ex_dt': exp_date,
                'ls_ct': count
                }
    
            res = requests.post(url=STOCK, data=data)
            print("입고 DB 전송 결과 :", res)


else:
    st.error('바코드를 다시 입력해주세요.')