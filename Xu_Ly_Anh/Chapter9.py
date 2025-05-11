import cv2
import numpy as np
L = 256

def Erosion(imgin):
    w = cv2.getStructuringElement(cv2.MORPH_RECT, (45, 45))
    imgout = cv2.erode(imgin, w)
    return imgout

def Dilation(imgin):
    w = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    imgout = cv2.dilate(imgin, w)
    return imgout

def Boundary(imgin):
    w = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    temp = cv2.erode(imgin, w)
    imgout = imgin - temp
    return imgout

def Contour(imgin):
    #bắt buộc imagin phải là ảnh nhị phân: có 2 màu: đen 0 và trắng 255
    M, N = imgin.shape
    imgout = cv2.cvtColor(imgin, cv2.COLOR_GRAY2BGR)
    contours, _ = cv2.findContours(imgin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contour = contours[0]
    n = len(contour)
    for i in range(n-1):
        x1 = contour[i][0][0]
        y1 = contour[i][0][1]
        x2 = contour[i+1][0][0]
        y2 = contour[i+1][0][1]
        cv2.line(imgout, (x1, y1), (x2, y2), (0, 0, 255), 1)

    x1 = contour[n-1][0][0]
    y1 = contour[n-1][0][1]
    x2 = contour[0][0][0]
    y2 = contour[0][0][1]
    cv2.line(imgout, (x1, y1), (x2, y2), (0, 0, 255), 1)

    return imgout


def CountRice(imgin):
    w = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (81,81))
    temp = cv2.morphologyEx(imgin, cv2.MORPH_TOPHAT, w)
    ret, temp = cv2.threshold(temp, 100, L-1, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    temp = cv2.medianBlur(temp, 3)
    dem, label = cv2.connectedComponents(temp)
    text = 'Co %d hat gao' % (dem-1) 
    print(text)
    a = np.zeros(dem, np.int16)
    M, N = label.shape
    color = 150
    for x in range(0, M):
        for y in range(0, N):
            r = label[x, y]
            a[r] = a[r] + 1
            if r > 0:
                label[x,y] = label[x,y] + color

    for r in range(0, dem):
        print('%4d %10d' % (r, a[r]))

    max = a[1]
    rmax = 1
    for r in range(2, dem):
        if a[r] > max:
            max = a[r]
            rmax = r

    xoa = np.array([], np.int16)
    for r in range(1, dem):
        if a[r] < 0.5*max:
            xoa = np.append(xoa, r)

    for x in range(0, M):
        for y in range(0, N):
            r = label[x,y]
            if r > 0:
                r = r - color
                if r in xoa:
                    label[x,y] = 0
    label = label.astype(np.uint8)
    cv2.putText(label,text,(1,25),cv2.FONT_HERSHEY_SIMPLEX,1.0, (255,255,255),2)
    return label
