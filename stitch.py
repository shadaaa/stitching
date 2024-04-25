import cv2

image1 = cv2.imread("C:/Users/ASUS/OneDrive/Desktop/scene.jpg")
image2 = cv2.imread("C:/Users/ASUS/OneDrive/Desktop/2.jpg")
gray1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
gray2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
sift = cv2.SIFT_create()
kp1 , des1 = sift.detectAndCompute(gray1,None)
kp2, des2 = sift.detectAndCompute(gray2, None)
bf = cv2.BFMatcher()
matches = bf. knnMatch(des1, des2, k=2)
good_matches = []
for m,n in matches:
    if m.distance < 0.75 * n.distance:
        good_matches.append(m)
import numpy as np
if len(good_matches) > 10:
    src_pts = np.float32([kp1[m.queryIdx].pt for m in good_matches]).reshape(-1,1,2)
    dst_pts = np.float32([kp2[m.trainIdx].pt for m in good_matches]).reshape(-1,1,2)
    H, _ = cv2.findHomography(src_pts,dst_pts,cv2.RANSAC,5.0)
    h, w = gray2.shape
    stitched_image = cv2.warpPerspective(image1, H, (w + image1.shape[1],h))
    stitched_image[0:h, 0:w] = image2
    cv2.imwrite('stitched_image.jpg',stitched_image)
    cv2.imshow('Stitched Image',stitched_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

else:
    print("Not enough good matches to create a stitched image.")
