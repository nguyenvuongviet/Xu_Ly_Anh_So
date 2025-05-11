import cv2
import time
import os
import finger.hand as htm
import streamlit as st

st.set_page_config(
    page_title="Đếm ngón tay",
    page_icon="🖐️",
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

st.title('🖐️ Đếm ngón tay')

with st.container():
    st.subheader("📷 Điều khiển Camera")
    camera_on = st.toggle("📷 Bật/Tắt Camera", key="cam_toggle")

    if not st.session_state.cam_toggle:
        st.markdown("""
        <div class="notification-box">
            <span style="font-size:1.4rem; margin-right:8px;">🔇</span>
            <span>Camera đang <strong>tắt</strong>. Bật lên để sử dụng tính năng đếm ngón tay.</span>
        </div>
        """, unsafe_allow_html=True)

    FolderPath="finger/Fingers"
    lst=os.listdir(FolderPath)
    lst = sorted(lst, key=lambda x: int(x.split(".")[0]))  
    print(lst)  # ['1.png', '2.png', '3.png', '4.png', '5.png', '6.png']

    lst_2=[]  # khai báo list chứa các mảng giá trị của các hình ảnh/
    for i in lst:
        image=cv2.imread(f"{FolderPath}/{i}")  # Fingers/1.jpg , Fingers/2.jpg ...
        lst_2.append(image)

    if st.session_state.cam_toggle:
        cap=cv2.VideoCapture(1) # nếu có nhiều cam thì thêm id webcam  1,2,3..
        if not cap.isOpened():
            st.error("Không thể kết nối với camera. Vui lòng kiểm tra lại.")
            st.session_state.cam_toggle = False

        pTime=0

        detector = htm.handDetector(detectionCon=0.55)

        fingerid= [4,8,12,16,20]
        video_placeholder = st.image([])

        while st.session_state.cam_toggle:
            ret,frame =cap.read()
            if not ret:
                st.error("Không thể đọc khung hình từ camera. Vui lòng kiểm tra lại.")
                break

            frame = detector.findHands(frame)
            lmList = detector.findPosition(frame, draw=False) # phát hiện vị trí

            if len(lmList) !=0:
                fingers= []
                # viết cho ngón cái (ý tường là điểm 4 ở bên trái hay bên phải điểm 2 )
                if lmList[fingerid[0]][1] < lmList[fingerid[0] - 1][1]:
                    fingers.append(1)
                else:
                    fingers.append(0)
                # viết cho 4 ngón dài
                for id in range(1,5):
                    if lmList[fingerid[id]][2] < lmList[fingerid[id]-2][2]:
                        fingers.append(1)
                    else:
                        fingers.append(0)

                songontay=fingers.count(1)
                print(songontay)
                h, w, c = lst_2[songontay-1].shape
                frame[0:h,0:w] = lst_2[songontay-1]  # nếu số ngón tay =0 thì lst_2[-1] đẩy về phần tử cuối cùng của list là ảnh 6

                # vẽ thêm hình chữ nhật hiện số ngón tay
                cv2.rectangle(frame,(0,200),(150,400),(0,255,0),-1)
                cv2.putText(frame,str(songontay),(30,390),cv2.FONT_HERSHEY_PLAIN,10,(255,0,0),5)

            cTime=time.time()  # trả về số giây, tính từ 0:0:00 ngày 1/1/1970 theo giờ  utc , gọi là(thời điểm bắt đầu thời gian)
            fps=1/(cTime-pTime) # tính fps Frames per second - đây là  chỉ số khung hình trên mỗi giây
            pTime=cTime
            # show fps lên màn hình, fps hiện đang là kiểu float , ktra print(type(fps))
            cv2.putText(frame, f"FPS: {int(fps)}",(150,70),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),3)

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            video_placeholder.image(frame)
            if cv2.waitKey(1)== ord("q"): # độ trễ 1/1000s , nếu bấm q sẽ thoát
                break
        
        cap.release() # giải phóng camera
        cv2.destroyAllWindows() # thoát tất cả các cửa sổ
        st.success("Camera đã tắt")