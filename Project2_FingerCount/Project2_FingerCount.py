import cv2
import time
from mediapipe_HandDetectionModule import HandDetection
import math

#########################################
wCam, hCam = 640, 480
pTime = 0
########################################

hand_detector = HandDetection(max_num_hands=1, min_detection_confidence=0.7)
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
volume = 0
texts = '0'
count = 0

while True:
    ret, frame = cap.read()
    count = 0
    frame = hand_detector.detectHand(frame)  # Detect Hand
    lm = hand_detector.handLandmark(frame, False)  # Detect all landmark of hand

    cv2.rectangle(frame, (20, 70), (280, 340), (0, 0, 255), 3)
    if len(lm) != 0:

        # if lm[4][2] < lm[2][2]:
        #     count += 1
        # if lm[8][2] < lm[6][2]:
        #     count += 1
        # if lm[12][2] < lm[10][2]:
        #     count += 1
        # if lm[16][2] < lm[14][2]:
        #     count += 1
        # if lm[20][2] < lm[18][2]:
        #     count += 1


        x1, y1 = lm[0][1], lm[0][2]
        x2, y2 = lm[5][1], lm[5][2]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        cv2.circle(frame, (cx, cy), 5, (255, 0, 255), -1)

        thumb_length = math.hypot(cx - lm[4][1], cy - lm[4][2])
        index_finger_length = math.hypot(cx - lm[8][1], cy - lm[8][2])
        middle_finger_length = math.hypot(cx - lm[12][1], cy - lm[12][2])
        ring_finger_length = math.hypot(cx - lm[16][1], cy - lm[16][2])
        pinky_finger_length = math.hypot(cx - lm[20][1], cy - lm[20][2])

        # print(f'thumb_length:{thumb_length}')
        # print(f'index_finger_length:{index_finger_length}')
        # print(f'middle_finger_length:{middle_finger_length}')
        # print(f'ring_finger_length:{ring_finger_length}')
        # print(f'pinky_finger_length:{pinky_finger_length}')
        if thumb_length > 95:
            count += 1
        if index_finger_length > 140:
            count += 1
        if middle_finger_length > 140:
            count += 1
        if ring_finger_length > 140:
            count += 1
        if pinky_finger_length > 110:
            count += 1

    cv2.putText(frame, f"Count:{count}", (440, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    # Calculate FPS
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(frame, f"FPS:{int(fps)}", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    cv2.imshow('Final', frame)

    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
