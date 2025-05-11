import cv2
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Nhận dạng màu sắc",
    page_icon="🎨",
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
        .stCheckbox {
            background-color: #2d2d44 !important;
            border: 3px solid #ff9a44;
            border-radius: 12px !important;
            padding: 12px !important;
            box-shadow: 0 2px 8px rgba(255, 154, 68, 0.3);
            margin-bottom: 20px;
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
        .stCheckbox > div > label {
            color: #ffffff !important;
            font-weight: bold;
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

st.title('🎨 Nhận dạng màu sắc')

def loadmausac():
    with st.container():
        st.subheader("📷 Điều khiển Camera")
        camera_on = st.toggle("📷 Bật/Tắt Camera", key="cam_toggle")

        if not st.session_state.cam_toggle:
            st.markdown("""
            <div class="notification-box">
                <span style="font-size:1.4rem; margin-right:8px;">🔇</span>
                <span>Camera đang <strong>tắt</strong>. Bật lên để sử dụng tính năng nhận diện.</span>
            </div>
            """, unsafe_allow_html=True)
        else:
            cap = cv2.VideoCapture(1)
            if not cap.isOpened():
                st.error("Không thể kết nối với camera. Vui lòng kiểm tra lại.")
                st.session_state.cam_toggle = False
                return
            
            cap.set(3, 720)
            cap.set(4, 1280)
            
            video_placeholder = st.image([])
            while st.session_state.cam_toggle:
                ret, frame = cap.read()
                if not ret:
                    st.error("Không thể đọc khung hình từ camera. Vui lòng kiểm tra lại.")
                    break
                
                frame = cv2.flip(frame, 1)
                
                x, y = int(frame.shape[1] / 2), int(frame.shape[0] / 2)
                b, g, r = frame[y, x]
                b, g, r = int(b), int(g), int(r)
                
                color_name = getColorName(b, g, r)
                drawSquare(frame, x, y)
                putText(frame, x, y, color_name, b, g, r)
                
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                video_placeholder.image(frame)
                
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            
            cap.release()
            cv2.destroyAllWindows()

def drawSquare(img, x, y):
    YELLOW = (0, 255, 255)
    BLUE = (255, 225, 0)
    
    cv2.line(img, (x - 150, y - 150), (x - 100, y - 150), YELLOW, 2)
    cv2.line(img, (x - 150, y - 150), (x - 150, y - 100), BLUE, 2)
    
    cv2.line(img, (x + 150, y - 150), (x + 100, y - 150), YELLOW, 2)
    cv2.line(img, (x + 150, y - 150), (x + 150, y - 100), BLUE, 2)
    
    cv2.line(img, (x + 150, y + 150), (x + 100, y + 150), YELLOW, 2)
    cv2.line(img, (x + 150, y + 150), (x + 150, y + 100), BLUE, 2)
    
    cv2.line(img, (x - 150, y + 150), (x - 100, y + 150), YELLOW, 2)
    cv2.line(img, (x - 150, y + 150), (x - 150, y + 100), BLUE, 2)
    
    cv2.circle(img, (x, y), 5, (255, 255, 153), -1)

index = ["color", "color_name", "hex", "R", "G", "B"]
csv = pd.read_csv("Nhan_Dien_Mau_Sac/colors.csv", names=index, header=None)

def getColorName(b, g, r):
    minimum = 1000 
    cname = None
    for i in range(len(csv)):
        d = abs(b - int(csv.loc[i, "B"])) + abs(g - int(csv.loc[i, "G"])) + abs(r - int(csv.loc[i, "R"]))
        if d <= minimum:
            minimum = d
            cname = csv.loc[i, "color_name"]
    return cname

def putText(img, x, y, color_name, b, g, r):
    cv2.rectangle(img, (x - 150, y - 220), (x + 300, y - 170), (b, g, r), -1)
    text = f"{color_name} | R={r} G={g} B={b}"
    cv2.putText(img, text, (x - 140, y - 190), cv2.FONT_HERSHEY_COMPLEX, 0.7, (255, 255, 255), 2)

loadmausac()