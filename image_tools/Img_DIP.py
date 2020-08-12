import numpy as np
import cv2


class ImgDIP(object):
    '''
    Image use, this program can setting lower and upper bounds that image colors you want to get,
    the setting mode can be RGB, HSV
    '''

    def __init__(self, img=None, img_path=None):
        if img is None and img_path is not None:
            self.img = cv2.imread(img_path)
        elif img is None:
            print("Error, this class need to choise img or img_path to import")

        self.img = img
        self.img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    def split_channels(self, img=None):
        if img is None:
            img = self.img

        C1, C2, C3 = cv2.split(img)
        return C1, C2, C3

    def merge_channels(self, C1, C2, C3):
        img = cv2.merge([C1, C2, C3])
        return img

    def increase_1channel_value(self, channel, NUM_INCREASE):
        rows = channel.shape[0]
        cols = channel.shape[1]

        for row in range(rows):
            for col in range(cols):
                item = channel[row, col]
                item += NUM_INCREASE
                if item > 255:
                    item = 255
                channel[row, col] = item

        return channel


def convert_hsv(image, isShow=True):
    hsv_img = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    H, S, V = hsv_img[:, :, 0], hsv_img[:, :, 1], hsv_img[:, :, 2]
    #(H, S, V) = split_color(image, False)
    if isShow:
        cv2.imshow("Original", image)
        cv2.imshow("HSV", hsv_img)
        cv2.imshow("H", H)
        cv2.imshow("S", S)
        cv2.imshow("V", V)
        cv2.waitKey(0)
    return hsv_img, H, S, V


def get_square_img(img):
    square_size = max(img.shape[:])
    square_center = int(square_size / 2)
    output_img = np.zeros(
        (square_size, square_size), dtype='uint8')
    start_point_x = square_center - int(img.shape[0]/2)
    start_point_y = square_center - int(img.shape[1]/2)
    output_img[start_point_x: start_point_x + img.shape[0],
               start_point_y: start_point_y + img.shape[1]] = img

    return output_img


def get_biggest_countour(img, isShow=False):
    contours = get_contours_binary(img, THRESH_VALUE=100, whiteGround=False)
    new_contours = []
    contour_area_list = []
    for contour in contours:
        contour_area = cv2.contourArea(contour)
        if contour_area > (img.size * 0.05) and contour_area < (img.size * 0.95) and contour.size > 8:
            contour_area_list.append(contour_area)
            new_contours.append(contour)

    if len(contour_area_list) != 0:
        biggest_contour = [
            new_contours[contour_area_list.index(max(contour_area_list))]]
    else:
        # need to fix : no contour fit the constrain
        biggest_contour = []
        # print(filename)

    if isShow is True:
        bgr_img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        bgr_img = cv2.drawContours(
            bgr_img, biggest_contour, -1, (0, 255, 0), 3)
        cv2.imshow('biggest_contour', bgr_img)
        # cv2.waitKey(0)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            pass

    return biggest_contour


def remove_img_nosie(img, contours, isShow=False):
    '''
        Only save contours part, else place become back.
        ===
        create a np.zeros array(black),
        use cv2.drawContours() make contours part become 255 (white),
        final, use cv2.gitwise_and() to remove noise for img
    '''
    crop_img = np.zeros(img.shape, dtype="uint8")
    crop_img = cv2.drawContours(
        crop_img.copy(), contours, -1, 255, thickness=-1)
    crop_img = cv2.bitwise_and(img, crop_img)

    if isShow is True:
        cv2.imshow('remove_img_nosie', crop_img)
        # cv2.waitKey(0)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            pass
    return crop_img
