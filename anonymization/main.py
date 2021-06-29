from collections import deque

import click
import cv2
import mediapipe as mp
import numpy as np
import pandas as pd
from loguru import logger

from .config import cfg

@click.command()
@click.option("--device", default=0, type=int, help="id of camera to use")
def command_line(device: int) -> None:
    """perform basic face detection and liveness estimation"""

    mp_drawing = mp.solutions.drawing_utils
    mp_face_mesh = mp.solutions.face_mesh

    d_spec = mp_drawing.DrawingSpec(
        thickness=1, circle_radius=1, color=(0, 255, 0)
    )

    cap = cv2.VideoCapture(device)

    mins = []
    with mp_face_mesh.FaceMesh(
        min_detection_confidence=cfg.min_detection_confidence,
        min_tracking_confidence=cfg.min_tracking_confidence,
    ) as face_mesh:

        while cap.isOpened():
            success, image = cap.read()
            if not success:
                logger.info("Ignoring empty camera frame.")
                # If loading a video, use 'break' instead of 'continue'.
                continue

            # Flip the image horizontally for a later selfie-view display, and convert
            # the BGR image to RGB.
            image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)

            blur = cv2.GaussianBlur(image,(cfg.blur_amount, cfg.blur_amount),0)

            # To improve performance, optionally mark the image as not writeable to
            # pass by reference.
            image.flags.writeable = False
            results = face_mesh.process(image)

            # Draw the face mesh annotations on the image.
            image.flags.writeable = True
            if results.multi_face_landmarks:
                for face_landmarks in results.multi_face_landmarks:

                    landmarks = np.array([(p.x, p.y) for p in face_landmarks.landmark])                    
                    face_min = np.min(landmarks * image.shape[:2][::-1], axis=0).astype(np.int)
                    face_max = np.max(landmarks * image.shape[:2][::-1], axis=0).astype(np.int)
                    s = np.s_[face_min[1]:face_max[1], face_min[0]:face_max[0], :]
                    image[s] = blur[s]

           
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            cv2.imshow("anonymization", image)
            if cv2.waitKey(5) & 0xFF == 27:
                break
    cap.release()
