import numpy as np
import cv2

L = 256
def Spectrum(imgin):
    M, N = imgin.shape
    P = cv2.getOptimalDFTSize(M)
    Q = cv2.getOptimalDFTSize(N)
    fp = np.zeros((P,Q), np.float32)
    fp[:M,:N] = imgin
    fp = fp/(L-1)
    for x in range(0, M):
        for y in range(0, N):
            if (x+y) % 2 == 1:
                fp[x,y] = -fp[x,y]
    F = cv2.dft(fp, flags = cv2.DFT_COMPLEX_OUTPUT)
    S = np.sqrt(F[:,:,0]**2 + F[:,:,1]**2)
    S = np.clip(S, 0, L-1)
    return S.astype(np.uint8)

def FrequencyFilter(imgin):
    M, N = imgin.shape
    P = cv2.getOptimalDFTSize(M)
    Q = cv2.getOptimalDFTSize(N)
    fp = np.zeros((P,Q), np.float32)
    fp[:M,:N] = imgin
    for x in range(0, M):
        for y in range(0, N):
            if (x+y) % 2 == 1:
                fp[x,y] = -fp[x,y]
    F = cv2.dft(fp, flags = cv2.DFT_COMPLEX_OUTPUT)
    H = np.zeros((P,Q), np.float32)
    D0 = 60
    n = 2
    for u in range(0, P):
        for v in range(0, Q):
            Duv = np.sqrt((u-P//2)**2 + (v-Q//2)**2)
            if Duv > 0:
                H[u,v] = 1.0/(1.0 + np.power(D0/Duv,2*n))
    G = F.copy()
    for u in range(0, P):
        for v in range(0, Q):
            G[u,v,0] = F[u,v,0]*H[u,v]
            G[u,v,1] = F[u,v,1]*H[u,v]
    g = cv2.idft(G, flags = cv2.DFT_SCALE)
    gp = g[:,:,0]
    for x in range(0, P):
        for y in range(0, Q):
            if (x+y)%2 == 1:
                gp[x,y] = -gp[x,y]
    imgout = gp[0:M,0:N]
    return np.clip(imgout,0,L-1).astype(np.uint8)

# def CreateNotchRejectFilter():
#     P = 250
#     Q = 180
#     D0 = 10
#     n = 2
#     H = np.ones((P,Q), np.float32)
#     coords = [(44, 58), (40, 119), (86, 59), (82, 119)]
#     for u in range(P):
#         for v in range(Q):
#             h = 1.0
#             for (ui, vi) in coords:
#                 for du, dv in [(ui, vi), (P-ui, Q-vi)]:
#                     Duv = np.sqrt((u-du)**2 + (v-dv)**2)
#                     h *= 1.0/(1.0 + np.power(D0/Duv,2*n)) if Duv > 0 else 0.0
#             H[u,v] = h
#     return H

def CreateNotchRejectFilter(P, Q):
    D0 = 10
    n = 2
    H = np.ones((P, Q), np.float32)
    coords = [(44, 58), (40, 119), (86, 59), (82, 119)]
    for u in range(P):
        for v in range(Q):
            h = 1.0
            for (ui, vi) in coords:
                for du, dv in [(ui, vi), (P-ui, Q-vi)]:
                    Duv = np.sqrt((u-du)**2 + (v-dv)**2)
                    h *= 1.0 / (1.0 + np.power(D0 / Duv, 2 * n)) if Duv > 0 else 0.0
            H[u, v] = h
    return H

# def DrawNotchRejectFilter():
#     H = CreateNotchRejectFilter()
#     return (H*(L-1)).astype(np.uint8)
def DrawNotchRejectFilter():
    P, Q = 250, 180
    H = CreateNotchRejectFilter(P, Q)
    return (H * (L - 1)).astype(np.uint8)


def RemoveMoire(imgin):
    M, N = imgin.shape
    P = cv2.getOptimalDFTSize(M)
    Q = cv2.getOptimalDFTSize(N)
    fp = np.zeros((P,Q), np.float32)
    fp[:M,:N] = imgin
    for x in range(0, M):
        for y in range(0, N):
            if (x+y) % 2 == 1:
                fp[x,y] = -fp[x,y]
    F = cv2.dft(fp, flags = cv2.DFT_COMPLEX_OUTPUT)
    # H = CreateNotchRejectFilter()
    H = CreateNotchRejectFilter(P, Q)
    G = F.copy()
    for u in range(0, P):
        for v in range(0, Q):
            G[u,v,0] = F[u,v,0]*H[u,v]
            G[u,v,1] = F[u,v,1]*H[u,v]
    g = cv2.idft(G, flags = cv2.DFT_SCALE)
    gp = g[:,:,0]
    for x in range(0, P):
        for y in range(0, Q):
            if (x+y)%2 == 1:
                gp[x,y] = -gp[x,y]
    imgout = gp[0:M,0:N]
    return np.clip(imgout,0,L-1).astype(np.uint8)
