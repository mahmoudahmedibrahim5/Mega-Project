import sys
import os
import cv2
import numpy as np

# Read both images and convert to grayscale
# img1 = cv.imread('left_img.png', cv.IMREAD_GRAYSCALE)
# img2 = cv.imread('right_img.png', cv.IMREAD_GRAYSCALE)

# if len(sys.argv) <= 2:
#     print("disparity_map.py img_left img_right")
#     exit(0)

# img1 = cv2.imread(sys.argv[1], cv2.IMREAD_GRAYSCALE)
#
# img2 = cv2.imread(sys.argv[2], cv2.IMREAD_GRAYSCALE)

def stereo(img1_path, img2_path, i):
    img1 = cv2.imread(img1_path, cv2.IMREAD_GRAYSCALE)
    img2 = cv2.imread(img2_path, cv2.IMREAD_GRAYSCALE)
    # cv2.imshow("1", img1)
    # cv2.imshow("2", img2)
    # cv2.waitKey(0)
    # exit(0)
    # ------------------------------------------------------------
    # PREPROCESSING

    # Compare unprocessed images
    # fig, axes = plt.subplots(1, 2, figsize=(15, 10))
    # axes[0].imshow(img1, cmap="gray")
    # axes[1].imshow(img2, cmap="gray")
    # axes[0].axhline(250)
    # axes[1].axhline(250)
    # axes[0].axhline(450)
    # axes[1].axhline(450)
    # plt.suptitle("Original images")
    # plt.savefig("original_images.png")
    # plt.show()

    # cv2.waitKey(0)
    # exit(0)
    # 1. Detect keypoints and their descriptors
    # Based on: https://docs.opencv.org/master/dc/dc3/tutorial_py_matcher.html

    # Initiate SIFT detector
    sift = cv2.SIFT_create()
    # find the keypoints and descriptors with SIFT
    kp1, des1 = sift.detectAndCompute(img1, None)
    kp2, des2 = sift.detectAndCompute(img2, None)

    # Visualize keypoints
    imgSift = cv2.drawKeypoints(
        img1, kp1, None, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    # cv.imshow("SIFT Keypoints", imgSift)
    # cv.imwrite("sift_keypoints.png", imgSift)

    # Match keypoints in both images
    # Based on: https://docs.opencv.org/master/dc/dc3/tutorial_py_matcher.html
    FLANN_INDEX_KDTREE = 1
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    search_params = dict(checks=50)  # or pass empty dictionary
    flann = cv2.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(des1, des2, k=2)

    # Keep good matches: calculate distinctive image features
    # Lowe, D.G. Distinctive Image Features from Scale-Invariant Keypoints. International Journal of Computer Vision 60, 91–110 (2004). https://doi.org/10.1023/B:VISI.0000029664.99615.94
    # https://www.cs.ubc.ca/~lowe/papers/ijcv04.pdf
    matchesMask = [[0, 0] for i in range(len(matches))]
    good = []
    imgPointsLeft = []
    imgPointsRight = []

    for i, (m, n) in enumerate(matches):
        if m.distance < 0.7 * n.distance:
            # Keep this keypoint pair
            matchesMask[i] = [1, 0]
            good.append(m)
            imgPointsRight.append(kp2[m.trainIdx].pt)
            imgPointsLeft.append(kp1[m.queryIdx].pt)

    # Draw the keypoint matches between both pictures
    # Still based on: https://docs.opencv.org/master/dc/dc3/tutorial_py_matcher.html
    draw_params = dict(matchColor=(0, 255, 0),
                       singlePointColor=(255, 0, 0),
                       matchesMask=matchesMask[300:500],
                       flags=cv2.DrawMatchesFlags_DEFAULT)

    keypoint_matches = cv2.drawMatchesKnn(
        img1, kp1, img2, kp2, matches[300:500], None, **draw_params)

    # cv.imshow("Keypoint matches", keypoint_matches)
    # cv.imwrite("keypoint_matches.png", keypoint_matches)

    # ------------------------------------------------------------
    # STEREO RECTIFICATION

    # Calculate the fundamental matrix for the cameras
    # https://docs.opencv.org/master/da/de9/tutorial_py_epipolar_geometry.html
    imgPointsLeft = np.int32(imgPointsLeft)
    imgPointsRight = np.int32(imgPointsRight)
    fundamental_matrix, inliers = cv2.findFundamentalMat(imgPointsLeft, imgPointsRight, cv2.FM_RANSAC)

    # We select only inlier points
    imgPointsLeft = imgPointsLeft[inliers.ravel() == 1]
    imgPointsRight = imgPointsRight[inliers.ravel() == 1]

    def drawlines(img1src, img2src, lines, pts1src, pts2src):
        ''' img1 - image on which we draw the epilines for the points in img2
            lines - corresponding epilines '''
        r, c = img1src.shape
        img1color = cv2.cvtColor(img1src, cv2.COLOR_GRAY2BGR)
        img2color = cv2.cvtColor(img2src, cv2.COLOR_GRAY2BGR)
        # Edit: use the same random seed so that two images are comparable!
        np.random.seed(0)
        for r, pt1, pt2 in zip(lines, pts1src, pts2src):
            color = tuple(np.random.randint(0, 255, 3).tolist())
            x0, y0 = map(int, [0, -r[2] / r[1]])
            x1, y1 = map(int, [c, -(r[2] + r[0] * c) / r[1]])
            img1color = cv2.line(img1color, (x0, y0), (x1, y1), color, 1)
            img1color = cv2.circle(img1color, tuple(pt1), 5, color, -1)
            img2color = cv2.circle(img2color, tuple(pt2), 5, color, -1)
        return img1color, img2color

    # Find epilines corresponding to points in right image (second image) and
    # drawing its lines on left image
    lines1 = cv2.computeCorrespondEpilines(
        imgPointsRight.reshape(-1, 1, 2), 2, fundamental_matrix)
    lines1 = lines1.reshape(-1, 3)
    img5, img6 = drawlines(img1, img2, lines1, imgPointsLeft, imgPointsRight)

    # Find epilines corresponding to points in left image (first image) and
    # drawing its lines on right image
    lines2 = cv2.computeCorrespondEpilines(
        imgPointsLeft.reshape(-1, 1, 2), 1, fundamental_matrix)
    lines2 = lines2.reshape(-1, 3)
    img3, img4 = drawlines(img2, img1, lines2, imgPointsRight, imgPointsLeft)

    # plt.subplot(121), plt.imshow(img5)
    # plt.subplot(122), plt.imshow(img3)
    # plt.suptitle("Epilines in both images")
    # plt.savefig("epilines.png")
    # plt.show()

    # Stereo rectification (uncalibrated variant)
    # Adapted from: https://stackoverflow.com/a/62607343
    h1, w1 = img1.shape
    h2, w2 = img2.shape
    _, H1, H2 = cv2.stereoRectifyUncalibrated(
        np.float32(imgPointsLeft), np.float32(imgPointsRight), fundamental_matrix, imgSize=(w1, h1)
    )

    # Rectify (undistort) the images and save them
    # Adapted from: https://stackoverflow.com/a/62607343
    img1_rectified = cv2.warpPerspective(img1, H1, (w1, h1))
    img2_rectified = cv2.warpPerspective(img2, H2, (w2, h2))
    # cv.imwrite("rectified_1.png", img1_rectified)
    # cv.imwrite("rectified_2.png", img2_rectified)

    # Draw the rectified images
    # fig, axes = plt.subplots(1, 2, figsize=(15, 10))
    # axes[0].imshow(img1_rectified, cmap="gray")
    # axes[1].imshow(img2_rectified, cmap="gray")
    # axes[0].axhline(250)
    # axes[1].axhline(250)
    # axes[0].axhline(450)
    # axes[1].axhline(450)
    # plt.suptitle("Rectified images")
    # plt.savefig("rectified_images.png")
    # plt.show()

    # ------------------------------------------------------------
    # CALCULATE DISPARITY (DEPTH MAP)
    # Adapted from: https://github.com/opencv/opencv/blob/master/samples/python/stereo_match.py
    # and: https://docs.opencv.org/master/dd/d53/tutorial_py_depthmap.html

    # StereoSGBM Parameter explanations:
    # https://docs.opencv.org/4.5.0/d2/d85/classcv_1_1StereoSGBM.html

    # Matched block size. It must be an odd number >=1 . Normally, it should be somewhere in the 3..11 range.
    block_size = 11
    min_disp = -128
    max_disp = 128
    # Maximum disparity minus minimum disparity. The value is always greater than zero.
    # In the current implementation, this parameter must be divisible by 16.
    num_disp = max_disp - min_disp
    # Margin in percentage by which the best (minimum) computed cost function value should "win" the second best value to consider the found match correct.
    # Normally, a value within the 5-15 range is good enough
    uniquenessRatio = 5
    # Maximum size of smooth disparity regions to consider their noise speckles and invalidate.
    # Set it to 0 to disable speckle filtering. Otherwise, set it somewhere in the 50-200 range.
    speckleWindowSize = 200
    # Maximum disparity variation within each connected component.
    # If you do speckle filtering, set the parameter to a positive value, it will be implicitly multiplied by 16.
    # Normally, 1 or 2 is good enough.
    speckleRange = 2
    disp12MaxDiff = 0

    stereo = cv2.StereoSGBM_create(
        minDisparity=min_disp,
        numDisparities=num_disp,
        blockSize=block_size,
        uniquenessRatio=uniquenessRatio,
        speckleWindowSize=speckleWindowSize,
        speckleRange=speckleRange,
        disp12MaxDiff=disp12MaxDiff,
        P1=8 * 1 * block_size * block_size,
        P2=32 * 1 * block_size * block_size,
    )
    disparity_SGBM = stereo.compute(img1_rectified, img2_rectified)

    # plt.imshow(disparity_SGBM, cmap='plasma')
    # plt.colorbar()
    # plt.show()

    # Normalize the values to a range from 0..255 for a grayscale image
    disparity_SGBM = cv2.normalize(disparity_SGBM, disparity_SGBM, alpha=255,
                                   beta=0, norm_type=cv2.NORM_MINMAX)
    disparity_SGBM = np.uint8(disparity_SGBM)

    # cv2.imshow("Disparity", disparity_SGBM)

    cv2.imwrite(f"out/stereo/disparity_grayscale_{i}.png", disparity_SGBM)

    cv2.waitKey()
    cv2.destroyAllWindows()

    # TODO
    # from cameramatrix calibrate to find depth
    # where depth = baseline * focal / disparity
    # from depth we can find the length also


i = 1
mainFolder = "images/stereo"
myFolders = os.listdir(mainFolder)
for file in myFolders:
    path = mainFolder + "/" + file
    images = os.listdir(path)
    x, y = images
    x_path = f"{path}/{x}"
    y_path = f"{path}/{y}"
    img = cv2.imread(x_path, cv2.IMREAD_GRAYSCALE)
    print(x_path, y_path)
    stereo(x_path, y_path, i)
    i += 1
