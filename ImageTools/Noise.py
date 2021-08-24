import cv2
import skimage
import numpy as np


def get_pepper_salt_noised(img, amount=0.05, isShow=False):
    # img = cv2.cvtColor(cvImg, cv2.COLOR_BGR2RGB)
    img = img / 255.0  # floating point image
    img_noised = skimage.util.random_noise(img, 's&p', amount=amount)
    img_noised = np.uint8(img_noised * 256)
    # img_noised = cv2.cvtColor(img_noised, cv2.COLOR_BGR2RGB)
    if isShow:
        cv2.imshow("Pepper_salt_noise: " + str(amount), img_noised)
        cv2.waitKey(0)
    return img_noised


def img_gaussian_noised(cvImg, var=0.01, isShow=False):
    img = cv2.cvtColor(cvImg, cv2.COLOR_BGR2RGB)
    img = img / 255.0  # floating point image
    img_noised = skimage.util.random_noise(img, 'gaussian', var=var)
    img_noised = np.uint8(img_noised * 256)
    cvImg_noised = cv2.cvtColor(img_noised, cv2.COLOR_BGR2RGB)
    if isShow:
        cv2.imshow("Gaussian_noised: " + str(var), cvImg_noised)
        cv2.waitKey(0)
    return cvImg_noised


def img_speckle_noised(cvImg, var=0.01, isShow=False):
    img = cv2.cvtColor(cvImg, cv2.COLOR_BGR2RGB)
    img = img / 255.0  # floating point image
    img_noised = skimage.util.random_noise(img, 'speckle', var=var)
    img_noised = np.uint8(img_noised * 256)
    cvImg_noised = cv2.cvtColor(img_noised, cv2.COLOR_BGR2RGB)
    if isShow:
        cv2.imshow("Speckle_noised: " + str(var), cvImg_noised)
        cv2.waitKey(0)
    return cvImg_noised


# Median filter
def median_filter(img, K_size=3):  # img = 讀取圖片;K = 表示核大小，必須是>1的奇數
    H, W, C = img.shape
    # Zero padding
    pad = K_size // 2
    out = np.zeros((H + pad * 2, W + pad * 2, C), dtype=np.float)
    out[pad : pad + H, pad : pad + W] = img.copy().astype(np.float)
    tmp = out.copy()  # 複製影像

    # filtering
    for y in range(H):
        for x in range(W):
            for c in range(C):
                out[pad + y, pad + x, c] = np.median(tmp[y : y + K_size, x : x + K_size, c])
    out = out[pad : pad + H, pad : pad + W].astype(np.uint8)
    return out


# Mean filter
def mean_filter(img, G=3):  # img = 讀取圖片;G = 核大小(W,H) ex:(3,3) or (5,5)
    out = img.copy()  # 複製影像
    H, W, C = img.shape
    Nh = int((H) / G)
    Nw = int((W) / G)
    for y in range(Nh):
        for x in range(Nw):
            for c in range(C):
                out[G * y : G * (y + 1), G * x : G * (x + 1), c] = np.mean(out[G * y : G * (y + 1), G * x : G * (x + 1), c]).astype(
                    np.int
                )
    return out


if __name__ == "__main__":
    img_path = "./lena.jpg"
    img = cv2.imread(img_path, -1)
    # for i in range(1, 4, 1):
    #     cvImg_noised = img_pepper_salt_noised(img, i *0.01)
    # return
    for i in range(0, 3, 1):
        cvImg_noised = img_gaussian_noised(img, i * 0.01)

    # for i in range(0, 3, 1):
    #     cvImg_noised = img_speckle_noised(img, i *0.01)
    # return
