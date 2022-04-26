import cv2
import numpy as np


class CameraDIP(object):
    '''
    Camera use, this program can setting lower and upper bounds that camera colors you want to get,
    the setting mode can be RGB, HSV
    '''

    def __init__(self, capID=None):
        if capID is None:
            capID = 0
        self.capID = capID

    def show_cap_inRGB_boundary(self, lower_color_bounds=None, upper_color_bounds=None, isShow=True):
        if lower_color_bounds is None:
            lower_color_bounds = np.array([0, 0, 0])
        if upper_color_bounds is None:
            upper_color_bounds = np.array([255, 255, 255])

        # RGB2BGR
        lower_color_bounds = np.array([lower_color_bounds[2], lower_color_bounds[1], lower_color_bounds[0]])
        upper_color_bounds = np.array([upper_color_bounds[2], upper_color_bounds[1], upper_color_bounds[0]])

        self.cap = cv2.VideoCapture(self.capID)  # 開啟 camera
        while True:
            # capture frame-by-frame
            ret, frame = self.cap.read()

            mask = cv2.inRange(frame, lower_color_bounds, upper_color_bounds)

            channels = frame.shape[2]
            for channel in range(channels):
                frame[:, :, channel] = frame[:, :, channel] & mask

            # display the resulting frameq

            if isShow is True:
                cv2.imshow("frame", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):  # 按q鍵退出
                break
        # when everything done , release the capture
        self.cap.release()
        cv2.destroyAllWindows()

    def show_cap_inHSV_boundary(self, lower_color_bounds=None, upper_color_bounds=None, isShow=True):
        if lower_color_bounds is None:
            lower_color_bounds = np.array([0, 0, 0])
        if upper_color_bounds is None:
            upper_color_bounds = np.array([127, 255, 255])

        self.cap = cv2.VideoCapture(self.capID)  # 開啟 camera
        while True:
            # capture frame-by-frame
            ret, frame = self.cap.read()

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(frame, lower_color_bounds, upper_color_bounds)

            channels = frame.shape[2]
            for channel in range(channels):
                frame[:, :, channel] = frame[:, :, channel] & mask

            frame = cv2.cvtColor(frame, cv2.COLOR_HSV2BGR)
            self.frame = frame
            # display the resulting frameq
            if isShow is True:
                cv2.imshow("frame", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):  # 按q鍵退出
                break
        # when everything done , release the capture
        self.cap.release()
        cv2.destroyAllWindows()

    def show_cap(self, subModule_name=None, isShow=True):
        '''
        This function has no mask, if you want to add mask to generate the frame you make,
        you can use variable:
        >>> subModule_name
        to make this happen,
        in variable "subModule_name" put filename relative path that you call this function,
        and in the filename that you input,
        create a function name call "get_mask_frame",
        push one input variable and one return variable into the function,
        input original frame, the other is the frame you generate,
        like this:
        >>> get_mask_frame(frame)
        '''
        self.cap = cv2.VideoCapture(self.capID)  # 開啟 camera

        while True:
            # capture frame-by-frame
            ret, self.frame = self.cap.read()

            if subModule_name is not None:
                subModule = __import__(subModule_name)
                frame = subModule.get_mask_frame(self.frame)
            else:
                frame = self.frame

            # display the resulting frameq
            if isShow is True:
                cv2.imshow("frame", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):  # 按q鍵退出
                break
        # when everything done , release the capture
        self.cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    a = CameraDIP()
    a.show_cap_inRGB()
