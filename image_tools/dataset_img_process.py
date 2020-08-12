import numpy as np
import cv2
import pydicom
from Model.find_file_name import get_filenames
from Model.BoundaryDescriptor import *


def get_dataset_paths(usr_imgs_path, NUM_DIVIDED=20):
    usr_img_paths = get_filenames(usr_imgs_path, 'dcm')
    num_img_list = []
    for usr_img_path in usr_img_paths:
        num_img = int(usr_img_path.split('/')[-1][:-4])
        num_img_list.append(num_img)
    num_img_list.sort()
    # print(num_img_list)

    dist = len(num_img_list) / NUM_DIVIDED
    dataset_img_paths = []
    for i in range(NUM_DIVIDED):
        num_img_path = '{}/{}.dcm'.format(usr_imgs_path,
                                          num_img_list[int(i * dist)])
        dataset_img_paths.append(num_img_path)

    return dataset_img_paths


def get_lung_img(img, isShow=False):
    lung_contour = get_biggest_countour(img, isShow=False)

    # detect image has black frame or not
    if len(lung_contour) != 0 and np.average(img[0:10, 0:10]) < 50:
        img = remove_black_frame(img, lung_contour, isShow=False)
        lung_contour = get_biggest_countour(img)

    lung_img = remove_img_nosie(img, lung_contour, isShow=False)
    features = calc_contour_feature(lung_img, lung_contour)
    lung_img = get_crop_img_list(lung_img, features)[0]

    if isShow:
        cv2.imshow('lung_img', lung_img)
        # cv2.waitKey(0)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            pass

    return lung_img
