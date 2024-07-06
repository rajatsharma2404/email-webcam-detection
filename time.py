import cv2
import streamlit as st
from time import strftime

st.title("Motion Detector")
start = st.button("Start Camera")

if start:
    streamlit_image = st.image([])
    camera = cv2.VideoCapture(0)

    while True:
        current_time = strftime("%I:%M:%S %p")
        current_date = strftime("%a, %d %b %Y")

        check, frame =camera.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        cv2.putText(img=frame,text=current_time,org=(30,50), fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=1.5, color=(255,255,255))
        cv2.putText(img=frame, text=current_date, org=(30, 70), fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=1.5,
                    color=(255, 255, 255))
        streamlit_image.image(frame)

        key = cv2.waitKey(1)
        if key == ord('q'):
            exit()

