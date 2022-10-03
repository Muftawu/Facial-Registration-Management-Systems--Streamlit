import cv2
import os
import time
import face_recognition as fr
import numpy as np
import streamlit as st
from database import InsertBlob
from cvzone.FaceDetectionModule import FaceDetector
from PIL import Image

detector = FaceDetector()


def pattern(frame):
    # frame = np.array(Image.open(frame))
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # frame = np.array(Image.open(frame))
    img, bbox = detector.findFaces(frame)

    if bbox:
        print(bbox[0]['score'])
        return img


def scan_face(path):
    global camera
    user_name = st.text_input("Enter new user name:  ", placeholder="User name")
    email = st.text_input("Enter email:  ", placeholder="email")
    # time.sleep(3)
    if user_name and email.endswith("gmail.com"):
        run = True
        time.sleep(2)
        st.subheader("Ready for Facial scan")
        FRAME_WINDOW = st.image([])
        camera = cv2.VideoCapture(0)
    else:
        run = False
    while run:
        ret, frame = camera.read()
        # frame = np.array(Image.open(frame))
        st.image(pattern(frame))
        camera.release()
        img_name = os.path.join(path, f"{user_name}.jpg")
        cv2.imwrite(img_name, frame)
        InsertBlob(img_name, user_name, email)
        run = False
        time.sleep(1)
        st.subheader("Scanned Image")
        st.subheader(f"...Scan Complete. Saved as {user_name.title()}")
        known_encodings, nameList = encode_scanned_faces(path)
        st.subheader("Encoding complete!")
        st.subheader("Please select a new option from the sidebar to continue..")


def stream_cam(run):
    # st.title("Webcam Live Feed")
    # run = st.checkbox('Run')
    FRAME_WINDOW = st.image([])
    camera = cv2.VideoCapture(0)
    while run:
        _, frame = camera.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        FRAME_WINDOW.image(frame)
    else:
        st.write('Stopped')


def encode_scanned_faces(images):
    imgList = os.listdir(images)
    nameList = []
    face_encodings = []
    for img in imgList:
        img = cv2.imread(f"{images}/{img}")
        encoding = fr.face_encodings(img)
        face_encodings.append(encoding)
    for i in imgList:
        nameList.append(os.path.splitext(i)[0])
    return face_encodings, nameList


def read_database(images):
    encd_vals, nameList = encode_scanned_faces(images)
    user_num = len(nameList)
    st.subheader("List of all registered Users")
    for i, (nm, en_val) in enumerate(zip(nameList, encd_vals)):
        i += 1
        st.write(f"{i}. {nm}\n")


def facial_recognition(images):
    global name
    FRAME_WINDOW = st.image([])
    camera = cv2.VideoCapture(0)
    run = True
    known_encodings, nameList = encode_scanned_faces(images)
    st.subheader("Number of encodings:   ")
    st.subheader(known_encodings)
    while run:
        ret, frame = camera.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        imgS = cv2.resize(frame, (0, 0), None, 0.25, 0.25)
        new_face_loc = fr.face_locations(imgS)
        new_face_encoding = fr.face_encodings(imgS, new_face_loc)

        for encodedFace, encodedLoc in zip(new_face_encoding, new_face_loc):
            # known_encodings, nameList = encode_scanned_faces(images)
            matches = fr.compare_faces(known_encodings, encodedFace)
            faceDis = fr.face_distance(known_encodings, encodedFace)

            st.subheader(faceDis)
            matchIndex = np.argmin(faceDis)
            st.subheader(matchIndex)

            if matches[matchIndex]:
                # st.subheader(matches[matchIndex])
                name = nameList[matchIndex].upper()
                # st.subheader(name), st.subheader(faceDis), st.subheader(matchIndex)

            y1, x2, y2, x1 = encodedLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(frame, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
            cv2.putText(frame, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 2)
            cv2.circle(frame, (100, 300), 10, (0, 255, 0), cv2.FILLED)

        FRAME_WINDOW.image(cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
