import streamlit as st
from webcam import webcam
import pyautogui
import requests
from post_processing import text_postprocessing
from func import ImageFile
import pyautogui
from config import DB_SERVER_URL


# 기본 설정
if 'count' not in st.session_state:
    st.session_state.count = 0
if 'last' not in st.session_state:
    st.session_state.last = None


st.markdown("<h1 style='text-align: center; color: blue;'>선 도 관 리</h1>", unsafe_allow_html=True)
option = st.selectbox("진행할 작업을 선택해주세요.", ("입고처리", "출고처리", "재고조회"))


if option == "입고처리":
    barcode = st.text_input("빈 칸에 바코드를 입력해주세요.")
    pyautogui.press("tab", presses=1, interval=0.2)
    st.header("")

    if len(barcode) == 13:
        # Create Radio Buttons
        check_cam = st.radio(label = '내장카메라 / 웹캠 여부를 선택하세요!!', options = ['Maincam', "Webcam"])
        st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
        
        image_file = ImageFile()

        if check_cam == 'Maincam': # 내장 캠인 경우
            captured_image = st.camera_input("카메라")
            
            if captured_image is None:
                st.write("Waiting for capture...")
            else:
                st.image(captured_image)

                if st.session_state.last != None: # 이전에 촬영된 이미지가 있는 경우
                    buffered_stream = image_file.image_to_buffer(st.session_state.last)
                    upload = {'file': buffered_stream}
                    # print(f"촬영된 이미지 정보는 {captured_image} 입니다.")
                    # print(f"이전에 촬영된 이미지 정보인 {st.session_state.last}가 전송됩니다.")
                    res = requests.post(url=DB_SERVER_URL, files=upload)
                    image_file.drop_image(buffered_stream)

                st.session_state.last = captured_image
                
        else: # 외장 캠인 경우
            captured_image = webcam("카메라")
            
            if captured_image is None:
                st.write("Waiting for capture...")
            else:
                st.session_state.count += 1
                st.image(captured_image)

                # 재촬영
                if st.session_state.last != None: # 이전에 촬영된 이미지가 있는 경우
                    buffered_stream = image_file.image_to_buffer(st.session_state.last)
                    upload = {'file': buffered_stream}
                    # print(f"촬영된 이미지 정보는 {captured_image} 입니다.")
                    # print(f"이전에 촬영된 이미지 정보인 {st.session_state.last}가 전송됩니다.")
                    res = requests.post(url=DB_SERVER_URL, files=upload)
                    image_file.drop_image(buffered_stream)
                
                st.session_state.last = captured_image

        # result = text_postprocessing(res)
        # print(result)


    if st.button('등록'):
        pyautogui.press("f5", presses=1, interval=0.2)