import os
import cv2
# mainFolder1 = "images"

# print(myFolders)

def stitch_custom(mainFolder="images/stitching"):
    myFolders = os.listdir(mainFolder)
    for folder in myFolders:
        path = mainFolder + '/' + folder

        images = []

        myList = os.listdir(path)

        print(f'Total no of images detected {len(myList)}')

        for imgName in myList:
            # print(imgN)
            currImg = cv2.imread(f'{path}/{imgName}')
            currImg = cv2.resize(currImg, (0, 0), None, 0.5, 0.5)
            images.append(currImg)

        stitcher = cv2.Stitcher_create(cv2.Stitcher_PANORAMA)
        status, result = stitcher.stitch(images)
        print(images)
        # print(myFolders)
        # print(myList)

        if status == cv2.STITCHER_OK:
            print("Generated")
            cv2.imshow(folder, result)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            cv2.imwrite(f'./out/stitching/{folder}.png', result)
        else:
            print("Failed")
        # print(len(images))