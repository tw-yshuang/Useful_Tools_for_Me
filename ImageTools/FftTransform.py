import cv2
import numpy as np


class ImgFftTransform(object):
    def __init__(self, path, laryer=None):
        if laryer is None:
            self.img = cv2.imread(path)
        else:
            self.img = cv2.imread(path, laryer)
        # simple averaging filter without scaling parameter
        self.mean = np.ones((3, 3))
        # creating a gaussian filter
        x = cv2.getGaussianKernel(5, 10)
        self.gaussian = x * x.T
        # different edge detecting filters
        # scharr in x-direction
        self.scharr = np.array([[-3, 0, 3], [-10, 0, 10], [-3, 0, 3]])
        # sobel in x direction
        self.sobel_x = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
        # sobel in y direction
        self.sobel_y = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])
        # laplacian
        self.laplacian = np.array([[0, 1, 0], [1, -4, 1], [0, 1, 0]])

        self.shun_crate = np.array(
            [[1 / (2 ** (1 / 2)), 1, 1 / (2 ** (1 / 2))], [1, -4 - 2 / (2 ** (1 / 2)), 1], [1 / (2 ** (1 / 2)), 1, 1 / (2 ** (1 / 2))]]
        )

    # 快速傅立葉變換（Fast Fourier Transform, FFT）
    def get_fft(self, img=None):
        if img is None:
            img = self.img

        fft = np.fft.fft2(img)

        return fft

    # fft + filter(濾波器)
    def get_fft_filter(self, filter_type, img=None):
        if img is None:
            img = self.img

        fft_filter = np.fft.fft2(filter_type, img.shape)

        return fft_filter

    def get_fft_shift(self, fft):
        fft_shift = np.fft.fftshift(fft)

        return fft_shift

    def get_magnitude_spectrum(self, fft, times_log=20):
        magnitude_spectrum = times_log * np.log(np.abs(fft))

        return magnitude_spectrum

    def get_ifft(self, fft):
        ifft = np.fft.ifft2(fft)
        real_ifft = np.real(ifft)
        return real_ifft, ifft

    def get_ifft_shift(self, ifft):
        ifft_shift = np.fft.ifftshift(ifft)

        return ifft_shift

    def get_homo_filter_ifft(self, img=None, filter_radius=20, rL=0.5, rH=2):
        if img is None:
            img = self.img
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = np.float32(cv2.cvtColor(img, cv2.COLOR_RGB2GRAY))
        rows, cols = img.shape
        rL = rL  # Low
        rH = rH  # High
        d0 = filter_radius  # filter size
        c = 2
        img_log = np.log(img + 1)
        fft = self.get_fft(img_log)  # image after log
        rows_center = np.floor(rows / 2)
        cols_center = np.floor(cols / 2)
        D = np.zeros((rows, cols))
        H = np.zeros((rows, cols))
        for i in range(rows):
            for j in range(cols):
                D[i, j] = (i - rows_center) ** 2 + (j - cols_center) ** 2
                H[i, j] = (rH - rL) * (np.exp(c * (-D[i, j] / (d0 ** 2)))) + rL
        print("D", D)
        # print("H",H)
        ifft = self.get_ifft(H * fft)
        ifft_exp = np.real(np.exp(ifft[0]))
        cv2.normalize(ifft_exp, 0, 1)
        return ifft_exp
