import cv2
import numpy as np
import imutils
import easyocr


def recognize_plate(self, img):
    # Apply grayscale

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply filter and get edges
    bfilter = cv2.bilateralFilter(gray, 11, 17, 17)
    edged = cv2.Canny(bfilter, 30, 200)

    # Find contours
    keypoints = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(keypoints)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]

    # Find contours that represent square
    location = None
    for contour in contours:
        approx = cv2.approxPolyDP(contour, 10, True)
        if len(approx) == 4:
            location = approx
            break

    # Apply mask to isolate license plate
    mask = np.zeros(gray.shape, np.uint8)

    # Find coordinates
    (x, y) = np.where(mask == 255)
    (x1, y1) = (np.min(x), np.min(y))
    (x2, y2) = (np.max(x), np.max(y))
    # Crop license plate
    cropped_image = gray[x1:x2 + 1, y1:y2 + 1]

    # OCR initialization
    reader = easyocr.Reader(['uk'])
    result = reader.readtext(cropped_image)

    # Get text
    text = result[0][-2]
    return text
