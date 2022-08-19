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

        contours, hierarchy = cv2.findContours(
            maskColor, retrievalMode, approxMode)

        if len(contours) > 0:
            for contour in contours:
                x, y, w, h = cv2.boundingRect(contour)
                # TODO clearer results ( maybe have a hashmap saves where are the contours and skip if its relatively
                #  small in distances.
                if w > 500 or h > 500 or w < 10 or h < 10:  # skip for really bing contours or small ones
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
    'star': [
        np.array([112, 93, 163]),
        np.array([132, 113, 243]),
    ],
    'colony': [
        np.array([155, 124, 162]),
        np.array([175, 144, 242]),
    ],
    'sponge': [
        np.array([80, 234, 76]),
        np.array([100, 254, 156]),
    ]
}
img1 = cv2.imread(sys.argv[1])

clr = ColorDetector(img1, colors)

clr.ColorContour(color='fragment', text='fragment')
clr.ColorContour(color='sponge', text='sponge')
clr.ColorContour(color='star', text='star')
clr.ColorContour(color='colony', text='colony')

cv2.imshow('res', clr.img)
cv2.waitKey(0)
