import streamlit as st
import argparse
import numpy as np
import os
import cv2
import torch
import torch.nn as nn
from torchvision import transforms
from PIL import Image

# === Page config & style ===
st.set_page_config(page_title="Nhận diện cảm xúc 😊", layout="wide")
st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(135deg, #1e1e2f, #2d2d44);
            color: #ffffff;
            font-family: 'Roboto', sans-serif;
            transition: all 0.3s ease;
        }
        .stApp.light-mode {
            background: linear-gradient(135deg, #e0f7fa, #ffffff);
            color: #333333;
        }
        h1 {
            color: #ffffff;
            text-align: center;
            background: linear-gradient(90deg, #ff6f61, #ff9a44);
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 4px 15px rgba(255, 111, 97, 0.4);
            margin-bottom: 30px;
            font-size: 2.2em;
        }
        h1.light-mode {
            color: #333333;
            background: linear-gradient(90deg, #ff8c61, #ffb347);
        }
        .stCheckbox {
            background-color: #2d2d44 !important;
            border: 3px solid #ff9a44;
            border-radius: 12px !important;
            padding: 12px !important;
            box-shadow: 0 2px 8px rgba(255, 154, 68, 0.3);
            transition: box-shadow 0.3s ease;
        }
        .stCheckbox.light-mode {
            background-color: #ffffff !important;
            border: 3px solid #ff8c61;
            box-shadow: 0 2px 8px rgba(255, 140, 97, 0.3);
        }
        .stCheckbox:hover {
            box-shadow: 0 4px 12px rgba(255, 154, 68, 0.5);
        }
        .stCheckbox > label {
            color: #ffffff !important;
            font-size: 1.2em;
            text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);
        }
        .stCheckbox input[type="checkbox"] {
            width: 20px;
            height: 20px;
            margin-right: 10px;
        }
        .element-container:has(> .stImage) {
            border: 2px solid #ff9a44;
            border-radius: 10px;
            padding: 10px;
            background-color: #1e1e2f;
            box-shadow: 0 4px 12px rgba(255, 154, 68, 0.3);
            margin-bottom: 20px;
        }
        .element-container:has(> .stImage).light-mode {
            border: 2px solid #ffb347;
            background-color: #f0f8ff;
            box-shadow: 0 4px 12px rgba(255, 179, 71, 0.3);
        }
        .css-1aumxhk {
            color: #ffffff;
        }
        .css-1aumxhk.light-mode {
            color: #333333;
        }
        .notification-box {
            background-color: #ffebee;
            color: #c62828;
            padding: 12px 20px;
            border-radius: 8px;
            font-size: 1.1rem;
            font-weight: 600;
            margin-top: 10px;
            border: 3px solid #ff9a44;
            display: flex;
            align-items: center;
            box-shadow: 0 2px 8px rgba(255, 154, 68, 0.3);
        }
        .notification-box.light-mode {
            background-color: #fff3f3;
            border: 3px solid #ff8c61;
            box-shadow: 0 2px 8px rgba(255, 140, 97, 0.3);
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1>😊 Nhận diện cảm xúc</h1>", unsafe_allow_html=True)

# === Argument parser ===
def str2bool(v):
    if v.lower() in ['on','yes','true','y','t']:
        return True
    elif v.lower() in ['off','no','false','n','f']:
        return False
    else:
        raise NotImplementedError

parser = argparse.ArgumentParser()
parser.add_argument('--scale','-sc', type=float, default=1.0)
parser.add_argument('--save','-s', type=str2bool, default=False)
args, _ = parser.parse_known_args()

# === Model definition ===
class EmotionCNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Conv2d(1,32,3,padding=1), nn.ReLU(), nn.MaxPool2d(2),
            nn.Conv2d(32,64,3,padding=1), nn.ReLU(), nn.MaxPool2d(2),
            nn.Conv2d(64,128,3,padding=1), nn.ReLU(), nn.MaxPool2d(2),
            nn.Flatten(),
            nn.Linear(128*6*6,256), nn.ReLU(), nn.Dropout(0.3),
            nn.Linear(256,7)
        )
    def forward(self,x):
        return self.net(x)

# === Load model & prepare ===
emotion_labels = ['Angry','Disgust','Fear','Happy','Sad','Surprise','Neutral']
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = EmotionCNN().to(device)
model_path = os.path.join(os.path.dirname(__file__),
                          '../Nhan_Dien_Cam_Xuc/emotion_cnn.pth')
model.load_state_dict(torch.load(model_path,map_location=device))
model.eval()

transform = transforms.Compose([
    transforms.Grayscale(),
    transforms.Resize((48,48)),
    transforms.ToTensor(),
    transforms.Normalize((0.5,),(0.5,))
])

# === Face detector ===
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades+'haarcascade_frontalface_default.xml'
)

# === UI: Toggle camera and placeholder ===
with st.container():
    st.subheader("📷 Điều khiển Camera")
    camera_on = st.toggle("📷 Bật/Tắt Camera", key="cam_toggle", value=False)

if not camera_on:
    st.markdown("""
    <div class="notification-box">
        <span style="font-size:1.4rem; margin-right:8px;">🔇</span>
        <span>Camera đang <strong>tắt</strong>. Bật lên để sử dụng tính năng nhận diện.</span>
    </div>
    """, unsafe_allow_html=True)
else:
    # Mở camera
    cap = cv2.VideoCapture(1)
    if not cap.isOpened():
        st.error("Không thể truy cập webcam.")
    else:
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            placeholder = st.image([], use_container_width=True)

        while st.session_state.cam_toggle:
            ret, frame = cap.read()
            if not ret:
                st.error("Không thể đọc khung hình từ camera.")
                break

            # Resize & gray
            frame = cv2.resize(frame,(0,0),fx=args.scale,fy=args.scale)
            gray  = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray,1.3,5)

            labels = []
            for (x,y,w,h) in faces:
                roi = frame[y:y+h, x:x+w]
                roi_pil = Image.fromarray(roi)
                inp = transform(roi_pil).unsqueeze(0).to(device)
                with torch.no_grad():
                    out = model(inp)
                    pred = torch.argmax(out,1).item()
                labels.append(emotion_labels[pred])

            # Vẽ box + label
            for (box,label) in zip(faces,labels):
                x,y,w,h = box
                cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
                cv2.putText(frame,label,(x,y-10),
                            cv2.FONT_HERSHEY_SIMPLEX,0.9,(36,255,12),2)

            # Show
            frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
            placeholder.image(frame, use_container_width=True)

        cap.release()
        cv2.destroyAllWindows()