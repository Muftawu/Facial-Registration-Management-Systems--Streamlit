import mediapipe.python.solutions as mp
from PIL import Image
import cv2
import numpy as np

mp_drawing = mp.drawing_utils
mp_face_mesh = mp.face_mesh

WHITE_COLOR = (224, 224, 224)
PINK_COLOR = (255, 0, 255)
BLACK_COLOR = (0, 0, 0)
RED_COLOR = (0, 0, 255)
GREEN_COLOR = (0, 128, 0)
BLUE_COLOR = (255, 0, 0)
drawing_spec = mp.drawing_utils.DrawingSpec(GREEN_COLOR, 1, 1)

demo_img = "muftawu.png"
demo_video = "facial.mp4"


def mesh(frame):
    face_count = 0
    with mp_face_mesh.FaceMesh(
            static_image_mode=True,
            max_num_faces=2,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
    ) as face_mesh:
        results = face_mesh.process(frame)

        out_img = frame.copy()
        out_img = cv2.cvtColor(out_img, cv2.COLOR_BGR2RGB)

        for face_landmarks in results.multi_face_landmarks:
            face_count += 1

            mp_drawing.draw_landmarks(out_img, face_landmarks,
                                      connections=mp_face_mesh.FACEMESH_CONTOURS,
                                      landmark_drawing_spec=drawing_spec)
    return out_img


if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    while True:
        _, frame = cap.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = mesh(frame)
        cv2.imshow('img', img)
        cv2.waitKey(1)
        # cap.release()
