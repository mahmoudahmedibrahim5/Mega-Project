import cv2
import sys
import numpy as np


class ColorDetector:

    def __init__(self, img, colors: {}):
        self.img = img
        self.colors = colors
        self.imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    def ColorContour(self, color: str, text: str, colorContour=(0, 0, 0), colorVal=1, font=cv2.FONT_HERSHEY_DUPLEX,
                     fontVal=1, retrievalMode=cv2.RETR_EXTERNAL, approxMode=cv2.CHAIN_APPROX_SIMPLE):
        maskColor = self.__doMask(color)

        kernel = np.ones((7, 7), np.uint8)
        maskColor = cv2.dilate(maskColor, kernel=kernel, iterations=4)

        contours, hierarchy = cv2.findContours(
            maskColor, retrievalMode, approxMode)

        if len(contours) > 0:
            for contour in contours:
                x, y, w, h = cv2.boundingRect(contour)
                # TODO clearer results ( maybe have a hashmap saves where are the contours and skip if its relatively
                #  small in distances.
                if w > 500 or h > 500 or w < 30 or h < 55:
                    # skip for really big contours or small ones
                    continue
                cv2.rectangle(self.img, (x, y),
                              (x + w, y + h), (139, 0, 139), 3)
                cv2.putText(self.img, text, (x, y), font,
                            fontVal, colorContour, colorVal)

    def __getMaskColorLower(self, color: str):
        try:
            return self.colors[color][0]
        except:
            print(f"could not find {color}")
            exit(1)

    def __getMaskColorUpper(self, color: str):
        try:
            return self.colors[color][1]
        except:
            print(f"could not find {color}")
            exit(1)

    def availableColors(self):
        return list(self.colors.keys())

    def __doMask(self, color: str):
        res = cv2.inRange(self.imgHSV, self.__getMaskColorLower(
            color), self.__getMaskColorUpper(color))

        return res


colors = {
    'fragment': [
        np.array([16, 232, 207]),
        np.array([36, 252, 287]),
    ],
    'star': [
        np.array([111, 86, 172]),
        np.array([131, 255, 255]),
    ],
    'colony': [
        np.array([155, 101, 187]),
        np.array([175, 121, 267]),
    ],
    'sponge': [
        np.array([102, 15, 199]),
        np.array([122, 35, 279]),
    ]
}
if len(sys.argv) == 1:
    print("python object_detector.py IMG_PATH.ext")
    exit(0)
img1 = cv2.imread(sys.argv[1])

clr = ColorDetector(img1, colors)

clr.ColorContour(color='fragment', text='fragment')
clr.ColorContour(color='sponge', text='sponge')
clr.ColorContour(color='star', text='star')
clr.ColorContour(color='colony', text='colony')

cv2.imshow('res', clr.img)
cv2.waitKey(0)
