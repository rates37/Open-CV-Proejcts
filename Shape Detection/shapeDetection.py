import cv2
import numpy as np

"""
Author: Satya Jhaveri
Purpose: detects and labels shapes on a white background
"""


def getContours(imgCanny, imgCpy) -> None:
    contours, hierarchy = cv2.findContours(imgCanny, mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_NONE)

    for contour in contours:
        # Getting the area of the current contour:
        area = cv2.contourArea(contour)

        # Only labelling the shape if its area is large enough (this filters out smaller contours detected in error):
        if area > 100:
            cv2.drawContours(imgCpy, contour, -1, (0,0,0), 3)  # Draws the contour in black with thickness 3

            perimeter = cv2.arcLength(contour, closed=True)
            polyApprox = cv2.approxPolyDP(contour, 0.02*perimeter, True)
            cornerCount = len(polyApprox)

            # Drawing a bounding box for the shape:
            x, y, width, height = cv2.boundingRect(polyApprox)
            cv2.rectangle(imgCpy, (x, y), (x+width, y+height), (0, 0, 255), 2)

            # Labelling the shapes:
            if cornerCount < 3:
                objType = "unknown"
            elif cornerCount == 3:
                objType = "triangle"
            elif cornerCount == 4:
                objType = "rectangle"
            elif cornerCount == 5:
                objType = "pentagon"
            else:
                objType = "circle"
            cv2.putText(imgCpy, objType, (x+(width//2) - 20, y+(height//2)), cv2.QT_FONT_NORMAL, 0.75, (0, 0, 0), 1)


def createCanny(image):
    # Converting image to black and white:
    imgGray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Blurring the image to increase the accuracy of the contour detection:
    imgBlur = cv2.GaussianBlur(imgGray, (7,7), 1)

    # Run canny image detection and return:
    return cv2.Canny(imgBlur, 50, 50)


if __name__ == "__main__":
    path = "res/shapes.png"

    img = cv2.imread(path)
    imgCpy = img.copy()
    imgCanny = createCanny(img)

    # Processing the image:
    getContours(imgCanny, imgCpy)

    # Displaying the image:
    cv2.imshow("original", img)
    cv2.imshow("Canny Processed", imgCanny)
    cv2.imshow("Processed", imgCpy)
    cv2.waitKey(0)

    # Saving the output file:
    cv2.imwrite("res/output.png", imgCpy)

