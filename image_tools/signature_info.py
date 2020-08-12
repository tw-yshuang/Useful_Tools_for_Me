import cv2
import numpy as np
import matplotlib.pyplot as plt


def get_contours_binary(img):
    imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    print(type(imgray))
    ret, thresh = cv2.threshold(imgray, 127, 255, 0)
    thresh_white = 255 - thresh

    # if your python-cv version is less than 4.0 the cv2.findContours will return 3 variable
    _, contours, hierarchy = cv2.findContours(
        thresh_white, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    return contours


def mark_center(contours, img=None, isShow=False):
    for i in contours:
        # calculate moments for each contour
        M = cv2.moments(i)
        if(M["m00"] == 0):
            M["m00"] = 1
        # calculate x,y coordinate of center
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])

        if isShow is True:
            # cv2.drawContours(img, [c], -1, (0, 255, 0), 2)
            img_center = cv2.circle(img, (cX, cY), 3, (20, 255, 0), -1)
            # cv2.putText(img, "centroid", (cX - 25, cY - 25),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            cv2.imshow("img_center", img_center)
            cv2.waitKey(0)

    return (cX, cY)


def get_signature_info(contours, center, isShow=False):
    cX, cY = center
    contours = np.array(contours)

    points = contours[0, :, 0, :]
    # print(points)

    start_point = 0
    for i in range(points.shape[0]):
        pX = points[i, 0]
        pY = points[i, 1]
        if cY == pY:
            if cX < pX:
                print(pX, pY)
                print("start")
                start_point = i
                break

    center_dist_infos = {}
    vecter_0 = np.array([points[start_point, 0] - cX, 0])
    for i in range(points.shape[0]):
        pX = points[i, 0]
        pY = points[i, 1]

        center_dist = (abs(cX-pX)**2 + abs(cY-pY)**2)**(1/2)
        vecter_a = np.array([points[i, 0] - cX, cY - points[i, 1]])

        # theta = np.degrees(np.arccos((vecter_0 - vecter_a) / vecter_0[0] * center_dist)) 錯的？？？
        theta = np.degrees(
            np.arccos(np.dot(vecter_0, vecter_a) / (vecter_0[0] * center_dist)))
        if pY > cY:
            theta = 360 - theta

        center_dist_infos.update({theta: center_dist})

    center_dist_infos_ls = sorted(
        center_dist_infos.items(), key=lambda x: x[0])
    center_dist_infos = {}
    for item in center_dist_infos_ls:
        center_dist_infos.update({item[0]: item[1]})

    if isShow is True:
        plt.clf()
        plt.xlim([0, 360])
        plt.ylim([0, max(center_dist_infos.values()) + 20])
        a = list(center_dist_infos.keys())
        b = list(center_dist_infos.values())
        plt.plot(a, b)
        plt.show()

    return center_dist_infos


if __name__ == "__main__":
    paths = ['images/square.jpg', 'images/pantagon.jpg', 'images/star.bmp']

    i = 0
    for path in paths:
        img = cv2.imread(path)
        contours = get_contours_binary(img)
        img_contours = cv2.drawContours(
            img.copy(), contours, -1, (0, 255, 0), 3)

        center = mark_center(contours)
        img_center = cv2.circle(img_contours, center, 3, (20, 255, 0), -1)

        signature_info = get_signature_info(contours, center, isShow=False)

        plt.subplot(3, 3, i+1)
        plt.imshow(img, cmap='gray', interpolation='bilinear')
        plt.title("oringal {}".format(
            path[7: -4])), plt.xticks([]), plt.yticks([])

        plt.subplot(3, 3, i+1+3)
        plt.imshow(img_contours, cmap='gray', interpolation='bilinear')
        plt.title("contours {}".format(
            path[7: -4])), plt.xticks([]), plt.yticks([])

        plt.subplot(3, 3, i+1+3+3)
        plt.title("signature {}".format(
            path[7: -4])), plt.xticks([]), plt.yticks([])
        plt.xlim([0, 360])
        y_min = min(signature_info.values())
        y_max = max(signature_info.values())
        plt.ylim([y_min - 10, y_max + 10])
        # plt.pcolor((0, 360, 45), (0, max(signature_info.values()) +
        #                           20, (max(signature_info.values()) + 20) / 10))
        a = list(signature_info.keys())
        b = list(signature_info.values())
        plt.plot(a, b)
        plt.xticks([0, 90, 180, 270, 360], [
                   r'$0$', r'$\pi/2$', r'$\pi$', r'2$\pi/3$', r'2$\pi$'])
        plt.yticks([y_min - 10, y_min + (y_max - y_min)/2, y_max + 10])

        i += 1
    plt.show()
