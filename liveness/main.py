import click
from loguru import logger
import cv2
import mediapipe as mp
import numpy as np

from .config import cfg
from collections import deque

@click.command()
@click.option("--device", default=0, type=int, help="id of camera to use")
def command_line(device: int) -> None:
    """perform basic face detection and liveness estimation"""

    mp_drawing = mp.solutions.drawing_utils
    mp_face_mesh = mp.solutions.face_mesh

    drawing_spec_ok = mp_drawing.DrawingSpec(thickness=1, circle_radius=1, color=(0,255,0))
    drawing_spec_nok = mp_drawing.DrawingSpec(thickness=1, circle_radius=1, color=(0,0,255))

    cap = cv2.VideoCapture(device)

    prev_faces = deque()

    with mp_face_mesh.FaceMesh(
            min_detection_confidence=cfg.min_detection_confidence,
            min_tracking_confidence=cfg.min_tracking_confidence) as face_mesh:

        while cap.isOpened():
            success, image = cap.read()
            if not success:
                logger.info("Ignoring empty camera frame.")
                # If loading a video, use 'break' instead of 'continue'.
                continue

            # Flip the image horizontally for a later selfie-view display, and convert
            # the BGR image to RGB.
            image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
            # To improve performance, optionally mark the image as not writeable to
            # pass by reference.
            image.flags.writeable = False
            results = face_mesh.process(image)

            # Draw the face mesh annotations on the image.
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            if results.multi_face_landmarks:
                for face_landmarks in results.multi_face_landmarks:


                    while len(prev_faces) >= cfg.face_history:
                        prev_faces.popleft()

                    landmarks = np.array([(p.x, p.y) for p in face_landmarks.landmark])
                    
                    if len(prev_faces) > 0:
                        transform, _ = cv2.estimateAffine2D(landmarks, prev_faces[-1])

                        landmarks_transformed = np.matmul(landmarks, transform)
                        error = np.linalg.norm(landmarks_transformed[:,:2] - prev_faces[-1], 2)
                        d_spec = drawing_spec_ok if error > cfg.liveness_threshold else drawing_spec_nok
                        mp_drawing.draw_landmarks(
                            image=image,
                            landmark_list=face_landmarks,
                            connections=mp_face_mesh.FACE_CONNECTIONS,
                            landmark_drawing_spec=d_spec,
                            connection_drawing_spec=d_spec,
                        )

                    prev_faces.append(landmarks)

            cv2.imshow("liveness", image)
            if cv2.waitKey(5) & 0xFF == 27:
                break
    cap.release()
