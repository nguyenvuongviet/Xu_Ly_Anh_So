import streamlit as st
import numpy as np
import cv2
from PIL import Image
import Xu_Ly_Anh.Chapter3 as c3
import Xu_Ly_Anh.Chapter4 as c4  # Giả sử các hàm chương 4 được định nghĩa trong file này
import Xu_Ly_Anh.Chapter9 as c9

st.set_page_config(page_title="Ứng dụng Xử lý Ảnh", page_icon="📸", layout="wide")

# CSS chung
st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(135deg, #1e1e2f, #2d2d44);
            color: #ffffff;
            font-family: 'Segoe UI', sans-serif;
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
        .stFileUploader, .stSelectbox, .stButton {
            background-color: #2d2d44 !important;
            border: 3px solid #ff9a44;
            border-radius: 12px !important;
            padding: 12px !important;
            box-shadow: 0 2px 8px rgba(255, 154, 68, 0.3);
            margin-bottom: 20px;
            transition: box-shadow 0.3s ease;
        }
        .stFileUploader.light-mode, .stSelectbox.light-mode, .stButton.light-mode {
            background-color: #ffffff !important;
            border: 3px solid #ff8c61;
            box-shadow: 0 2px 8px rgba(255, 140, 97, 0.3);
        }
        .stFileUploader:hover, .stSelectbox:hover, .stButton:hover {
            box-shadow: 0 4px 12px rgba(255, 154, 68, 0.5);
        }
        .stFileUploader > div > label, .stSelectbox > label {
            color: #ffffff !important;
            font-weight: bold;
            text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);
        }
        .stSelectbox > div > div {
            color: #ffffff;
            background-color: #2d2d44 !important;
            font-weight: 500;
        }
        .stSelectbox > div > div.light-mode {
            color: #333333;
            background-color: #ffffff !important;
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
        .notification-box span {
            font-size: 1.4rem;
            margin-right: 8px;
        }

        /* Căn giữa nội dung trong stFullScreenFrame */
        [data-testid="stFullScreenFrame"] {
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            height: 100%;
            padding: 20px;
        }

        [data-testid="stFullScreenFrame"] .stImage {
            text-align: center;
        }

        [data-testid="stFullScreenFrame"] .stImage > img {
            border-radius: 15px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
            max-width: 100%;
        }

        [data-testid="stFullScreenFrame"] .stCaption {
            text-align: center;
            color: #ffffff;
            margin-top: 10px;
            font-size: 16px;
        }

        /* Định dạng footer */
        .footer {
            text-align: center;
            color: #ffffff;
            font-size: 14px;
            margin-top: 50px;
            padding: 20px;
        }

        /* Links */
        a {
            color: #ff9a44 !important;
            text-decoration: none;
        }

        a:hover {
            text-decoration: underline;
        }

        /* Định dạng subheader */
        .stMarkdown h3 {
            color: #ff9a44;
            text-align: center;
            font-size: 1.5em;
            margin-top: 15px;
        }
    </style>
""", unsafe_allow_html=True)

# Title chung
st.markdown('<h1>📸 Ứng dụng Xử lý ảnh</h1>', unsafe_allow_html=True)

# --- Chọn chương xử lý ---
with st.container():
    st.subheader("📚 Chọn chương và kỹ thuật")
    chapter = st.selectbox("📚 Chọn chương:", ["Chương 3 - Miền không gian", "Chương 4 - Miền tần số", "Chương 9 - Hình thái học"])

    uploaded_file = st.file_uploader("📁 Chọn hình ảnh...", type=["jpg", "jpeg", "png", "tif"])

    # --- Lựa chọn kỹ thuật tương ứng ---
    if chapter == "Chương 3 - Miền không gian":
        technique = st.selectbox(
            "🛠️ Chọn kỹ thuật xử lý (Chương 3):",
            (
                "Negative",
                "Logarit",
                "Power",
                "PiecewiseLinear",
                "Histogram",
                "HistEqual",
                "HistEqualColor",
                "LocalHist",
                "HistStat",
                # "MyBoxFilter",
                "BoxFilter",
                "Threshold",
                "MedianFilter",
                "Sharpen",
                "Gradient"
            )
        )
    elif chapter == "Chương 4 - Miền tần số":
        technique = st.selectbox(
            "🛠️ Chọn kỹ thuật xử lý (Chương 4):",
            (
                "Spectrum",
                "FrequencyFilter",
                "RemoveMoire"
            )
        )
    elif chapter == "Chương 9 - Hình thái học":
        technique = st.selectbox(
            "🛠️ Chọn kỹ thuật xử lý (Chương 9):",
            (
                "Erosion",
                "Dilation",
                "Boundary",
                "CountRice"
            )
        )

    # Tạo hai cột để hiển thị hình ảnh
    col1, col2 = st.columns(2)

    if uploaded_file is not None:
        if chapter == "Chương 3 - Miền không gian":
            imgin = cv2.imdecode(np.frombuffer(uploaded_file.read(), np.uint8), cv2.IMREAD_GRAYSCALE)
            with col1:
                st.image(imgin, caption="📷 Hình ảnh gốc (Grayscale)", use_container_width=True)

            if technique == "Negative":
                processed_img = c3.Negative(imgin)
            elif technique == "Logarit":
                processed_img = c3.Logarit(imgin)
            elif technique == "Power":
                processed_img = c3.Power(imgin)
            elif technique == "PiecewiseLinear":
                processed_img = c3.PiecewiseLinear(imgin)
            elif technique == "Histogram":
                processed_img = c3.Histogram(imgin)
            elif technique == "HistEqual":
                processed_img = c3.HistEqual(imgin)
            elif technique == "HistEqualColor":
                image = Image.open(uploaded_file)
                frame = np.array(image)
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                processed_img = c3.HistEqualColor(frame)
                with col1:
                    st.image(frame, caption="📷 Hình ảnh gốc (RGB)", use_container_width=True)
            elif technique == "LocalHist":
                processed_img = c3.LocalHist(imgin)
            elif technique == "HistStat":
                processed_img = c3.HistStat(imgin)
            # elif technique == "MyBoxFilter":
            #     processed_img = c3.MyBoxFilter(imgin)
            elif technique == "BoxFilter":
                processed_img = c3.BoxFilter(imgin)
            elif technique == "Threshold":
                processed_img = c3.Threshold(imgin)
            elif technique == "MedianFilter":
                processed_img = c3.MedianFilter(imgin)
            elif technique == "Sharpen":
                processed_img = c3.Sharpen(imgin)
            elif technique == "Gradient":
                processed_img = c3.Gradient(imgin)

        elif chapter == "Chương 4 - Miền tần số":
            imgin = cv2.imdecode(np.frombuffer(uploaded_file.read(), np.uint8), cv2.IMREAD_GRAYSCALE)
            with col1:
                st.image(imgin, caption="📷 Hình ảnh gốc (Grayscale)", use_container_width=True)

            if technique == "Spectrum":
                processed_img = c4.Spectrum(imgin)
            elif technique == "FrequencyFilter":
                processed_img = c4.FrequencyFilter(imgin)
            elif technique == "RemoveMoire":
                processed_img = c4.RemoveMoire(imgin)

        elif chapter == "Chương 9 - Hình thái học":
            imgin = cv2.imdecode(np.frombuffer(uploaded_file.read(), np.uint8), cv2.IMREAD_GRAYSCALE)
            _, imgin = cv2.threshold(imgin, 128, 255, cv2.THRESH_BINARY)  # đảm bảo ảnh nhị phân
            with col1:
                st.image(imgin, caption="📷 Hình ảnh gốc (Nhị phân)", use_container_width=True)

            if technique == "Erosion":
                processed_img = c9.Erosion(imgin)
            elif technique == "Dilation":
                processed_img = c9.Dilation(imgin)
            elif technique == "Boundary":
                processed_img = c9.Boundary(imgin)
            elif technique == "CountRice":
                processed_img = c9.CountRice(imgin)

        with col2:
            st.image(processed_img, caption="🛠️ Hình ảnh sau xử lý", use_container_width=True)

    else:
        # Info message when no file is uploaded
        st.markdown(
            """
            <div class="notification-box">
                <span>ℹ️</span>
                <span>Vui lòng tải lên một bức ảnh để xử lý.</span>
            </div>
            """,
            unsafe_allow_html=True
        )
