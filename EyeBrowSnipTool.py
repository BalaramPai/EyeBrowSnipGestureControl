import cv2
import mediapipe
import time
import pyautogui as ss
import FaceMeshModule as fm

########################################################

# Initialize face mesh detector
detector = fm.FaceMeshDetection()

########################################################

# Variables for FPS calculation
cTime = 0
pTime = 0
# Webcam resolution
wCam = 640
hCam = 480
# Flag to track eyebrow raise state
isBlink = False
# List to store landmark positions
lmList = []

########################################################

# Start capturing video from webcam
cap = cv2.VideoCapture(0)
cap.set(3, wCam)  # Set camera width
cap.set(4, hCam)  # Set camera height

########################################################

while True:
    success, img = cap.read()  # Read frame from webcam
    img = cv2.flip(img, 1)  # Mirror the image

    img = detector.findMyFaceMesh(img)  # Draw face mesh on the image

    if detector.results.multi_face_landmarks:
        num = len(detector.results.multi_face_landmarks)  # Get number of detected faces

        for i in range(num):
            lmList = detector.faceMeshLocator(img, faceNo=i)  # Get landmarks for each face
            if (len(lmList)) != 0:
                a = lmList[23][2]  # Y-coordinate of landmark 23 (eyebrow)
                b = lmList[66][2]  # Y-coordinate of landmark 66 (eye)

                length = abs(a - b)  # Vertical distance between eyebrow and eye
                print(length)

                # If distance is large, eyebrow is raised
                if length >= 41:
                    if not isBlink:
                        isBlink = True  # Mark eyebrow raise start
                else:
                    if isBlink:
                        ss.screenshot(f"snap_{int(time.time())}.png")  # Take screenshot
                        print("screenshot taken")
                        isBlink = False  # Reset flag after screenshot

        cTime = time.time()  # Current time
        fps = 1 / (cTime - pTime)  # Calculate FPS
        pTime = cTime  # Update previous time

        # Display FPS on screen
        cv2.putText(img, f'FPS:{int(fps)}', (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        cv2.imshow('MyFace', img)  # Show the processed image
        cv2.waitKey(1)  # Wait for key press to update frame
