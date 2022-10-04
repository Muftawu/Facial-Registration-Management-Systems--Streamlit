from functions import scan_face
from functions import encode_scanned_faces
from functions import read_database
from functions import facial_recognition
from functions import stream_cam
import streamlit as st
import cv2
from database import RetrieveBlob
import numpy as np
import time
from PIL import Image

img_path = "./collected_imgs"
database_file = "./Database.txt"

# Scan face and take user ID
# scan_face(img_path)

# Encode all scanned faces
# print("Number of users: ", len(encoded_values))
# print(encoded_values, user_names)

# Display all scanned names
# read_database(img_path)

# Test our recognition
# facial_recognition(img_path)


# Stream feed form webcam
# stream_cam()

# encoded_values, user_names = encode_scanned_faces(img_path)
###########################################################

st.title("Registration Management System")

st.sidebar.title("Select an Option")
st.markdown("---")

# Activity widgets
actions = ['Home Page','Register New Customer', 'View all existing users', 'Authenticate existing users']
activity_option = st.sidebar.selectbox("Choose one", actions)


def mainloop():
    # encoded_values, user_names = encode_scanned_faces(img_path)
    if activity_option == actions[0]:  # HomePage
        st.subheader("Easily register your biometrics from anywhere")

    if activity_option == actions[1]:  # Scan new face
        scan_face(img_path)

        # RetrieveBlob()
        # encoded_values, user_names = encode_scanned_faces(img_path)

    if activity_option == actions[2]:  # List all Users
        encoded_values, user_names = encode_scanned_faces(img_path)
        print("Number of users: ", len(encoded_values))
        read_database(img_path)

    if activity_option == actions[3]:
        facial_recognition(img_path)

if __name__ == "__main__":
    mainloop()
