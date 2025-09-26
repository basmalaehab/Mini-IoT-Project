import cv2
import mediapipe as mp
import numpy as np
import pandas as pd
from datetime import datetime

mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils

def landmarks_to_embedding(landmarks, image_shape):
    ih, iw = image_shape[:2]
    embedding = []
    for lm in landmarks.landmark:
        embedding.append(lm.x * iw)
        embedding.append(lm.y * ih)
    return np.array(embedding)

def process_known_face(image_path):
    img = cv2.imread(image_path)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    with mp_face_mesh.FaceMesh(static_image_mode=True) as face_mesh:
        results = face_mesh.process(img_rgb)
        if results.multi_face_landmarks:
            return landmarks_to_embedding(results.multi_face_landmarks[0], img.shape)
    return None

def load_known_faces(people_dict):
    known_embeddings = []
    names = []
    for name, path in people_dict.items():
        embedding = process_known_face(path)
        if embedding is not None:
            known_embeddings.append(embedding)
            names.append(name)
        else:
            print(f"Face not detected for {name} in {path}")
    return known_embeddings, names

# ------------------ Main function ------------------
def recognize_faces(people_dict, attendance_file="attendance.csv", threshold=200):
    known_embeddings, names = load_known_faces(people_dict)

    try:
        attendance_df = pd.read_csv(attendance_file)
    except FileNotFoundError:
        attendance_df = pd.DataFrame(columns=["Name", "Time"])

    cap = cv2.VideoCapture(0)  

    with mp_face_mesh.FaceMesh(max_num_faces=1) as face_mesh:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = face_mesh.process(rgb_frame)

            if results.multi_face_landmarks:
                for face_landmarks in results.multi_face_landmarks:
                    embedding = landmarks_to_embedding(face_landmarks, frame.shape)

                    # Compare with known embeddings
                    min_dist = float('inf')
                    recognized_name = "Unknown"
                    for idx, known in enumerate(known_embeddings):
                        dist = np.linalg.norm(embedding - known)
                        if dist < min_dist:
                            min_dist = dist
                            if dist < threshold:
                                recognized_name = names[idx]

                    # Mark attendance if recognized
                    if recognized_name != "Unknown" and recognized_name not in attendance_df["Name"].values:
                        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        attendance_df = pd.concat([attendance_df, pd.DataFrame([[recognized_name, now]], columns=["Name", "Time"])], ignore_index=True)
                        attendance_df.to_csv(attendance_file, index=False)
                        print(f"{recognized_name} marked present at {now}")

                    # Draw landmarks and name
                    mp_drawing.draw_landmarks(frame, face_landmarks, mp_face_mesh.FACEMESH_CONTOURS)
                    cv2.putText(frame, recognized_name, (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

            cv2.imshow("Attendance System", frame)
            if cv2.waitKey(1) & 0xFF == 27:
                break

    cap.release()
    cv2.destroyAllWindows()
