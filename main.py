import os
import cv2

mainFolder = "images"

myFolders = os.listdir(mainFolder)

print(myFolders)

i = 0
for folder in myFolders:
    path = mainFolder + '/' + folder

    images = []

    myList = os.listdir(path)

    print(f'Total no of images detected {len(myList)}')

    for imgN in myList:
        # print(imgN)
        curImg = cv2.imread(f'{path}/{imgN}')
        curImg = cv2.resize(curImg, (0, 0), None, 0.2, 0.2)
        images.append(curImg)

    stitcher = cv2.Stitcher_create(cv2.Stitcher_PANORAMA)
    status, result = stitcher.stitch(images)

    if status == cv2.STITCHER_OK:
        print("Generated")
        cv2.imshow(folder, result)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        # cv2.imwrite(f'{i}.png',result)
        # i+=1
    else:
        print("Failed")
    print(len(images))
