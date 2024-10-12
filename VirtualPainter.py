import cv2
import numpy as np
import os
import HandTrackingModule as htm

#######################
brushThickness = 15
eraserThickness = 100
########################

folderPath = "Header2"
myList = os.listdir(folderPath)
print(myList)
overlayList = []

for imPath in myList:
    # Load image with transparency (if PNG with alpha channel)
    image = cv2.imread(f'{folderPath}/{imPath}', cv2.IMREAD_UNCHANGED)  # Use IMREAD_UNCHANGED for alpha channel
    
    if image.shape[2] == 4:  # Check if the image has an alpha channel (RGBA)
        # Resize the header
        header_resized = cv2.resize(image, (1280, 254))

        # Separate the RGB and alpha channels
        header_rgb = header_resized[:, :, :3]  # RGB channels
        alpha_channel = header_resized[:, :, 3]  # Alpha channel

        # Create a mask where the transparent areas are 0 and the rest is 1
        mask = alpha_channel.astype(np.uint8)
        
        # Append resized header (with transparency handling)
        overlayList.append((header_rgb, mask))
    else:
        print(f"Image {imPath} does not have an alpha channel.")

print(len(overlayList))
header_rgb, header_mask = overlayList[0]
drawColor = (255, 146, 3)

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = htm.handDetector(detectionCon=0.65, maxHands=1)
xp, yp = 0, 0
imgCanvas = np.zeros((720, 1280, 3), np.uint8)

while True:
    # 1. Import image
    success, img = cap.read()
    img = cv2.flip(img, 1)
    
    ############################
    # if header[4] (clicked) then reassign another header
    ############################

    # 2. Find Hand Landmarks
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img, draw=False)

    if len(lmList) != 0:
        detector.lmList = lmList  # Add this line

        # tip of index and middle fingers
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]

        # 3. Check which fingers are up
        fingers = detector.fingersUp()

        # 4. If Selection Mode - Two finger are up
        if fingers[1] and fingers[2]:
            if xp != 0 and yp != 0:
                xp, yp = 0, 0
            if y1 < 125:
                if 250 < x1 < 350:
                    header_rgb, header_mask = overlayList[0]
                    drawColor = (255, 146, 3)
                elif 400 < x1 < 500:
                    header_rgb, header_mask = overlayList[1]
                    drawColor = (0, 219, 29)
                elif 550 < x1 < 650:
                    header_rgb, header_mask = overlayList[2]
                    drawColor = (255, 212, 0)
                elif 700 < x1 < 800:
                    header_rgb, header_mask = overlayList[3]
                    drawColor = (0, 0, 254)
                elif 900 < x1 < 1000:
                    header_rgb, header_mask = overlayList[4]
                    drawColor = (0, 0, 0)
                elif 1100 < x1 < 1200:  # Reset
                    header_rgb, header_mask = overlayList[5]
                    imgCanvas = np.zeros((720, 1280, 3), np.uint8)
                
            cv2.rectangle(img, (x1, y1 - 25), (x2, y2 + 25), drawColor, cv2.FILLED)

        # 5. If Drawing Mode - Index finger is up
        if fingers[1] and fingers[2] == False:
            cv2.circle(img, (x1, y1), 15, drawColor, cv2.FILLED)
            if xp == 0 and yp == 0:
                xp, yp = x1, y1

            if drawColor == (0, 0, 0):
                cv2.line(img, (xp, yp), (x1, y1), drawColor, eraserThickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, eraserThickness)
            else:
                cv2.line(img, (xp, yp), (x1, y1), drawColor, brushThickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, brushThickness)

            xp, yp = x1, y1

    else:
        # Reset drawing points when no hand is detected
        xp, yp = 0, 0

    # Convert canvas to grayscale for bitwise operations
    imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
    _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
    img = cv2.bitwise_and(img, imgInv)
    img = cv2.bitwise_or(img, imgCanvas)

    # Setting the header image with transparency
    img[0:254, 0:1280] = cv2.bitwise_and(img[0:254, 0:1280], img[0:254, 0:1280], mask=cv2.bitwise_not(header_mask))
    img[0:254, 0:1280] = cv2.add(img[0:254, 0:1280], cv2.bitwise_and(header_rgb, header_rgb, mask=header_mask))

    # Display the result
    cv2.imshow("Image", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
