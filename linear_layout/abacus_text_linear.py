import sys
sys.path.append('../utils')
sys.path.append('../abacus_gesture_detection')

import mediapipe as mp
import cv2
import sys
from abacus_gesture_detection import AbacusGesture
from utils import TypingUtils

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)
frameWidth = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
frameHeight = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)



gestureToKeyMapping = {
    1: 'a', 2: 'b', 3: 'c', 4: 'd', 5: 'e', 6: 'f', 7: 'g', 8: 'h', 9: 'i', 10: 'j', 11: 'k', 12: 'l', 13: 'm', 14: 'n', 15: 'o', 16: 'p',
    17: 'q', 18: 'r', 19: 's', 20: 't', 21: 'u', 22: 'v', 23: 'w', 24: 'x', 25: 'y', 26: 'z',
    55: 'SPACE', 50: 'DELETE', 99: 'ENTER'
}

changeThreshold = 5
itr = 0
currentLetter = None
tempLetter = None
numSentence = 0
typedSentence = ''
xCoord = 100
inc = 10
typedChar = 0


abacusGesture = AbacusGesture()
typingUtils = TypingUtils()

with mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.8, max_num_hands=2) as hands:

    while cap.isOpened():
        # itr += 1
        ret, frame = cap.read()
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = cv2.flip(image, 1)
        image.flags.writeable = False
        results = hands.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        isLeft = False
        isRight = False
        
        left_hand_points = []
        right_hand_points = []

        cv2.putText(image, f'Entered:', (5, 60), cv2.FONT_HERSHEY_DUPLEX, 0.6, (0, 0, 0), 1)
        cv2.putText(image, f'{typedSentence}_', (120, 60), cv2.FONT_HERSHEY_DUPLEX, 0.6, (0, 0, 153), 1)

        if results.multi_hand_landmarks:
            for num, hand in enumerate(results.multi_hand_landmarks):
                if (results.multi_handedness[num].classification[0].label == 'Left'):
                    isLeft = True
                    for i in range(21):
                        left_hand_points.append([int(hand.landmark[i].x * frameWidth), int(hand.landmark[i].y * frameHeight), 1])

                if (results.multi_handedness[num].classification[0].label == 'Right'):
                    isRight = True
                    for i in range(21):
                        right_hand_points.append([int(hand.landmark[i].x * frameWidth), int(hand.landmark[i].y * frameHeight), 1])


            gesture = abacusGesture.getAbacusGesture(left_hand_points, right_hand_points, isLeft, isRight)

            try:
                letter = gestureToKeyMapping[gesture]
                if letter != tempLetter:
                    tempLetter = letter
                    itr = 0
                else:
                    if currentLetter != tempLetter:
                        itr += 1
                        if itr >= changeThreshold:
                            itr = 0
                            currentLetter = tempLetter
                if currentLetter != None:
                    cv2.putText(image, currentLetter, (xCoord, 85), cv2.FONT_HERSHEY_DUPLEX, 0.6, (255, 0, 0), 1)

            except Exception as e:
                if gesture == 0:
                    itr = 0
                    if currentLetter != None:

                        typedChar += 1
                        if currentLetter == 'ENTER':
                            numSentence += 1
                            typedSentence = ''
                            xCoord = 100
                            typedChar = 0

                            itr = 0
                        elif currentLetter == 'SPACE':
                            typedSentence += ' '
                            xCoord += inc
                        
                        elif currentLetter == 'DELETE':
                            if len(typedSentence) > 0:
                                typedSentence = typedSentence[:-1]
                                xCoord -= inc
                        
                        else:
                            typedSentence += currentLetter
                            xCoord += inc
                        
                        currentLetter = None
                        tempLetter = None
                else:
                    if tempLetter != None:
                        itr += 1
                        if itr >= changeThreshold:
                            tempLetter = None
                            currentLetter = None
                            itr = 0

        cv2.imshow('Test hand', image)

        if cv2.waitKey(1) == 27:
            break

cv2.destroyAllWindows()
cap.release()