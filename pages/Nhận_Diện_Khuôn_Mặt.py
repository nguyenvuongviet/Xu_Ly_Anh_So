import streamlit as st
import numpy as np
import cv2 as cv
import joblib
import os

st.set_page_config(
    page_title="Nhận diện khuôn mặt",
    page_icon="🧑‍💻",
    layout="wide"
)

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
        .stButton > button {
            background-color: #ff6f61;
            color: white;
            border: none;
            border-radius: 8px;
            padding: 8px 16px;
            font-weight: 600;
        }
        .stButton > button:hover {
            background-color: #e65b50;
            cursor: pointer;
        }
        .stButton > button.light-mode {
            background-color: #ff8c61;
        }
        .stButton > button.light-mode:hover {
            background-color: #e67e5b;
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
    </style>
""", unsafe_allow_html=True)

st.title('🧑‍💻 Nhận diện khuôn mặt')

FRAME_WINDOW = st.image([])

cap = cv.VideoCapture(1)

# Khởi tạo trạng thái stop
if 'stop' not in st.session_state:
    st.session_state.stop = False

# Nút nhận diện và dừng
with st.container():
    st.subheader("Điều khiển")
    col1, col2 = st.columns([1, 1])
    with col1:
        click = st.button("Nhận diện")
    with col2:
        press = st.button('Dừng lại')

if press:
    st.session_state.stop = not st.session_state.stop
    if st.session_state.stop:
        cap.release()
    else:
        cap = cv.VideoCapture(0)  # Mở lại camera khi tiếp tục

print('Trang thai nhan Stop', st.session_state.stop)

# Tải và kiểm tra stop.jpg
if 'frame_stop' not in st.session_state:
    stop_image_path = 'Nhan_Dien_Khuon_Mat/stop.jpg'
    if os.path.exists(stop_image_path):
        frame_stop = cv.imread(stop_image_path)
        if frame_stop is None:
            st.error(f"Không thể đọc file {stop_image_path}. Kiểm tra định dạng file.")
            st.session_state.frame_stop = None
        else:
            st.session_state.frame_stop = frame_stop
            print('Đã load stop.jpg')
    else:
        st.error(f"File {stop_image_path} không tồn tại.")
        st.session_state.frame_stop = None

# Hiển thị frame_stop khi stop == True
if st.session_state.stop:
    if st.session_state.frame_stop is not None:
        FRAME_WINDOW.image(st.session_state.frame_stop, channels='BGR')
    else:
        st.write("Không thể hiển thị ảnh dừng vì file stop.jpg không khả dụng.")

# Tải mô hình SVC
try:
    svc = joblib.load('Nhan_Dien_Khuon_Mat/svc.pkl')
except Exception as e:
    st.error(f"Không thể tải mô hình SVC: {e}")
    svc = None

mydict = ['cTrang', 'qhung', 'thly', 'vv', 'qv']

def visualize(input, faces, fps, thickness=2):
    if input is None:
        print("Error: Input frame is None")
        return input

    if faces is None or faces[1] is None or len(faces[1]) == 0:
        print("No faces detected")
        cv.putText(input, "No faces detected", (1, 50), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    else:
        for idx, face in enumerate(faces[1]):
            try:
                coords = face[:-1].astype(np.int32)
                cv.rectangle(input, (coords[0], coords[1]), (coords[0]+coords[2], coords[1]+coords[3]), (0, 255, 0), thickness)
                cv.circle(input, (coords[4], coords[5]), 2, (255, 0, 0), thickness)
                cv.circle(input, (coords[6], coords[7]), 2, (0, 0, 255), thickness)
                cv.circle(input, (coords[8], coords[9]), 2, (0, 255, 0), thickness)
                cv.circle(input, (coords[10], coords[11]), 2, (255, 0, 255), thickness)
                cv.circle(input, (coords[12], coords[13]), 2, (0, 255, 255), thickness)

                face_align = recognizer.alignCrop(input, face)
                if face_align is None:
                    print(f"Failed to align face {idx}")
                    continue
                face_feature = recognizer.feature(face_align)
                if face_feature is None:
                    print(f"Failed to extract features for face {idx}")
                    continue
                test_predict = svc.predict(face_feature)
                if len(test_predict) == 0:
                    print(f"No prediction for face {idx}")
                    continue
                result = mydict[test_predict[0]]
                cv.putText(input, result, (coords[0], coords[1]), cv.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 3)
            except Exception as e:
                print(f"Error processing face {idx}: {e}")
                continue

    cv.putText(input, f'FPS: {fps:.2f}', (20, 40), cv.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 3)
    return input

if __name__ == '__main__':
    if click and not st.session_state.stop:
        try:
            detector = cv.FaceDetectorYN.create(
                'Nhan_Dien_Khuon_Mat/face_detection_yunet_2023mar.onnx',
                "",
                (320, 320),
                0.9,
                0.3,
                5000)
            recognizer = cv.FaceRecognizerSF.create(
                'Nhan_Dien_Khuon_Mat/face_recognition_sface_2021dec.onnx', "")
        except Exception as e:
            st.error(f"Không thể tải mô hình phát hiện/nhận diện khuôn mặt: {e}")
            st.stop()

        tm = cv.TickMeter()
        frameWidth = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
        frameHeight = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
        detector.setInputSize([frameWidth, frameHeight])

        while True:
            if st.session_state.stop:
                break
            hasFrame, frame = cap.read()
            if not hasFrame:
                print('No frames grabbed!')
                break

            frame = cv.flip(frame, 1)
            tm.start()
            faces = detector.detect(frame)
            tm.stop()

            # Nhận diện khuôn mặt đầu tiên (nếu có)
            if faces[1] is not None and len(faces[1]) > 0:
                try:
                    face_align = recognizer.alignCrop(frame, faces[1][0])
                    if face_align is None:
                        print("Failed to align first face")
                    else:
                        face_feature = recognizer.feature(face_align)
                        if face_feature is None:
                            print("Failed to extract features for first face")
                        else:
                            test_predict = svc.predict(face_feature)
                            if len(test_predict) > 0:
                                result = mydict[test_predict[0]]
                                cv.putText(frame, result, (20, 70), cv.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 3)
                            else:
                                print("No prediction for first face")
                except Exception as e:
                    print(f"Error processing first face: {e}")

            # Vẽ kết quả
            frame = visualize(frame, faces, tm.getFPS())
            FRAME_WINDOW.image(frame, channels='BGR')