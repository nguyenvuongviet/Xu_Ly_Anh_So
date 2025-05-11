import os
from PIL import Image
from ultralytics import YOLO
import supervision as sv
import streamlit as st

# Kiểm tra cài đặt thư viện
import ultralytics

# Load the pre-trained YOLOv8 model
model = YOLO(
    "/Users/nguyenvuongviet/Downloads/Xu_Ly_Anh_So/TraiCay640x640_train/train_yolov8n/runs/detect/train/weights/best.pt"
)

st.set_page_config(
    page_title="Nhận diện trái cây",
    page_icon="🍎",
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
        .stFileUploader {
            background-color: #2d2d44 !important;
            border: 3px solid #ff9a44;
            border-radius: 12px !important;
            padding: 12px !important;
            box-shadow: 0 2px 8px rgba(255, 154, 68, 0.3);
            margin-bottom: 20px;
            transition: box-shadow 0.3s ease;
        }
        .stFileUploader.light-mode {
            background-color: #ffffff !important;
            border: 3px solid #ff8c61;
            box-shadow: 0 2px 8px rgba(255, 140, 97, 0.3);
        }
        .stFileUploader:hover {
            box-shadow: 0 4px 12px rgba(255, 154, 68, 0.5);
        }
        .stFileUploader > div > label {
            color: #ffffff !important;
            font-weight: bold;
            text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);
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

# Set page title
st.markdown('<h1>🍎 Dự Đoán Trái Cây với YOLOv8</h1>', unsafe_allow_html=True)

# Container chính chứa file uploader
with st.container():
    st.subheader("📤 Tải lên hình ảnh")
    
    uploaded_file = st.file_uploader("📁 Chọn hình ảnh...", type=["png", "jpg", "jpeg"])

    # Tạo hai cột để hiển thị hình ảnh
    col1, col2 = st.columns(2)

    if uploaded_file is not None:
        try:
            # Open the uploaded image
            image = Image.open(uploaded_file)

            # Hiển thị hình ảnh gốc trong cột 1
            with col1:
                st.image(image, caption="📷 Ảnh đã tải lên", use_container_width=True)

            # Progress spinner while making predictions
            with st.spinner("Đang dự đoán..."):
                # Perform prediction with confidence threshold of 0.25
                results = model.predict(image, conf=0.25)[0]

                # Convert the results into the 'supervision' format for annotations
                detections = sv.Detections.from_ultralytics(results)

                # Prepare the annotators
                box_annotator = sv.BoxAnnotator()
                label_annotator = sv.LabelAnnotator(text_color=sv.Color.BLACK)

                # Make a copy of the image to annotate
                annotated_image = image.copy()
                annotated_image = box_annotator.annotate(
                    annotated_image, detections=detections
                )
                annotated_image = label_annotator.annotate(
                    annotated_image, detections=detections
                )

                # Hiển thị hình ảnh đã xử lý trong cột 2
                with col2:
                    st.image(
                        annotated_image,
                        caption="🛠️ Ảnh dự đoán với YOLOv8",
                        use_container_width=True,
                    )

        except Exception as e:
            # Handle errors gracefully with a user-friendly message
            st.markdown(
                f"""
                <div class="notification-box">
                    <span>❌</span>
                    <span>Đã xảy ra lỗi: <strong>{e}</strong></span>
                </div>
                """,
                unsafe_allow_html=True
            )

    else:
        # Info message when no file is uploaded
        st.markdown(
            """
            <div class="notification-box">
                <span>ℹ️</span>
                <span>Vui lòng tải lên một bức ảnh để dự đoán.</span>
            </div>
            """,
            unsafe_allow_html=True
        )
