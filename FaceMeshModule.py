import cv2
import mediapipe as mp
import time

########################################################

# Creating a custom FaceMeshDetection class to handle face mesh detection.
class FaceMeshDetection():
    def __init__(self,
                 static_image_mode=False,
                 max_num_faces=2,
                 refine_landmarks=True,
                 min_detection_confidence=0.5,
                 min_tracking_confidence=0.5):
        # Setting up the face mesh parameters
        self.static_image_mode = static_image_mode
        self.max_num_faces = max_num_faces
        self.refine_landmarks = refine_landmarks
        self.min_detection_confidence = min_detection_confidence
        self.min_tracking_confidence = min_tracking_confidence

        # Initializing the MediaPipe FaceMesh module and drawing utilities
        self.module = mp.solutions.face_mesh
        self.obj = self.module.FaceMesh(self.static_image_mode,
                                        self.max_num_faces,
                                        self.refine_landmarks,
                                        self.min_detection_confidence,
                                        self.min_tracking_confidence)
        self.drawing_tool = mp.solutions.drawing_utils

    def findMyFaceMesh(self, img, draw=True):
        # Convert BGR image (OpenCV default) to RGB for MediaPipe
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.obj.process(imgRGB)

        # If faces are detected
        if self.results.multi_face_landmarks:
            for face in self.results.multi_face_landmarks:
                if draw:
                    # Draw face mesh contours on the original image
                    self.drawing_tool.draw_landmarks(img, face, self.module.FACEMESH_CONTOURS)
        return img

    def faceMeshLocator(self, img, faceNo=0):
        lmList = []

        # If any faces are detected
        if self.results.multi_face_landmarks:
            # Select the specified face (default: 0)
            myface = self.results.multi_face_landmarks[faceNo]

            # Iterate over all the landmarks in the selected face
            for id, lm in enumerate(myface.landmark):
                h, w, c = img.shape

                # Convert normalized coordinates to pixel coordinates
                cx, cy = int(lm.x * w), int(lm.y * h)

                # Append id and pixel coordinates to list
                lmList.append([id, cx, cy])
        return lmList

########################################################

def main():
    cTime = 0
    pTime = 0
    wCam = 640
    hCam = 480

    lmList = []

    # Start capturing video
    cap = cv2.VideoCapture(0)
    cap.set(3, wCam)  # Set width
    cap.set(4, hCam)  # Set height

    detector = FaceMeshDetection()

    while True:

        success, img = cap.read()
        img = cv2.flip(img, 1)  # Flip horizontally to act like a mirror

        img = detector.findMyFaceMesh(img)  # Draw face mesh

        if detector.results.multi_face_landmarks:
            num = len(detector.results.multi_face_landmarks)  # Count number of faces

            for i in range(num):
                lmList = detector.faceMeshLocator(img, faceNo=i)  # Get landmarks for each face
                if (len(lmList)) != 0:
                    print(lmList[1])  # Print one sample landmark

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        # Display FPS on the screen
        cv2.putText(img, f'FPS:{int(fps)}', (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        cv2.imshow('MyFace', img)
        cv2.waitKey(1)

########################################################

if __name__ == "__main__":
    main()
