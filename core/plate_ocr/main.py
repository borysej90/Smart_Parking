import cv2
import numpy as np
import imutils
import easyocr

class PlateRecognizer():
    """
        Plate number recognizer

        USAGE:
            Create class object and pass image to it using 'cv2.imread'
            Call 'recognize_plate' method to get text from plate

    """
    def __init__(self, image):
        self.img = image

    def recognize_plate(self):
        # Apply grayscale
        gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)

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

        # Apply mask to find license plate
        mask = np.zeros(gray.shape, np.uint8)
        new_image = cv2.drawContours(mask, [location], 0, 255, -1)
        new_image = cv2.bitwise_and(self.img, self.img, mask=mask)

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
