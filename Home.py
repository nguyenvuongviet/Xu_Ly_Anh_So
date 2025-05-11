import streamlit as st

st.set_page_config(page_title="Báo cáo cuối kỳ", layout="wide")
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
        .section-title {
            font-size: 28px;
            font-weight: bold;
            color: #ffffff;
            background: linear-gradient(90deg, #ff6f61, #ff9a44);
            padding: 20px;
            border-radius: 15px;
            text-align: center;
            margin-bottom: 30px;
            box-shadow: 0 4px 15px rgba(255, 111, 97, 0.4);
        }
        .section-title.light-mode {
            color: #333333;
            background: linear-gradient(90deg, #ff8c61, #ffb347);
        }
        .block {
            background-color: #2d2d44;
            border: 2px solid #ff9a44;
            border-radius: 15px;
            padding: 25px;
            margin-bottom: 30px;
            color: #ffffff;
            box-shadow: 0 4px 12px rgba(255, 154, 68, 0.3);
            height: 100%;
        }
        .block.light-mode {
            background-color: #f0f8ff;
            border: 2px solid #ffb347;
            color: #333333;
            box-shadow: 0 4px 12px rgba(255, 179, 71, 0.3);
        }
        .block h2 {
            font-size: 22px;
            margin-bottom: 20px;
            color: #ff9a44;
        }
        .block h2.light-mode {
            color: #ffb347;
        }
        .student-info {
            margin: 10px 0;
            font-size: 20px;
        }
        .toc-item {
            margin: 8px 0;
            font-size: 19px;
        }
        [data-testid="column"] {
            margin-right: 40px; /* Khoảng cách giữa các cột */
        }
        [data-testid="column"]:last-child {
            margin-right: 0;
        }
        /* Căn giữa nội dung trong stFullScreenFrame */
        [data-testid="stFullScreenFrame"] {
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            height: 100%;
        }
        [data-testid="stFullScreenFrame"] .stImage {
            text-align: center;
        }
        [data-testid="stFullScreenFrame"] .stImage > img {
            border-radius: 15px;
            box-shadow: 0 4px 12px rgba(255, 154, 68, 0.3);
            max-width: 100%;
        }
        [data-testid="stFullScreenFrame"] .stCaption {
            text-align: center;
            color: #ffffff;
            margin-top: 10px;
        }
    </style>

    <div class="section-title">
        👋 Chào mừng thầy đến với bài báo cáo cuối kỳ!
    </div>
""", unsafe_allow_html=True)

# Tạo bố cục 2 cột với khoảng cách
col1, col2 = st.columns([1, 1], gap="medium")

# Cột 1: Khối Sinh viên thực hiện và Mục lục
with col1:
    st.markdown("""
        <div class="block">
            <h2>📚 Sinh viên thực hiện</h2>
            <div class="student-info">🎓 Nguyễn Vương Việt - 22110457</div>
        </div>
                
        <div class="block">
            <h2>📋 Mục lục bài báo cáo:</h2>
            <div class="toc-item">😊 Nhận diện cảm xúc</div>
            <div class="toc-item">🧑‍💻 Nhận diện khuôn mặt</div>
            <div class="toc-item">🎨 Nhận diện màu sắc</div>
            <div class="toc-item">🍎 Nhận diện trái cây</div>
            <div class="toc-item">📸 Xử lý ảnh số</div>
            <div class="toc-item">🖐️ Đếm ngón tay</div>
        </div>
    """, unsafe_allow_html=True)

# Cột 2: Hình ảnh với st.image
with col2:
    st.image("Nguyen_Vuong_Viet.jpeg", caption="Ảnh sinh viên thực hiện", width=400)