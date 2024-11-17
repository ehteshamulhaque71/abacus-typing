import sys
sys.path.append('../utils')
sys.path.append('../abacus_gesture_detection')

import mediapipe as mp
import cv2

from t9_prediction import *
from abacus_gesture_detection import AbacusGesture
from utils import TypingUtils

# mappings


gestureToKeyMapping = {
    1: '1', 2: '2', 3: '3',
    4: '4', 5: '5', 6: '6',
    7: '7', 8: '8', 9: '9',
    55: 'SPACE', 50: 'DELETE', 99: 'ENTER',
    10: None, 20: None, 30: None, 40: None
}

# mediapipe and opencv setup
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)
frameWidth = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
frameHeight = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

# variables
changeThreshold = 5
itr = 0
currentLetter = None
tempLetter = None

typedSentence = ''
xCoord = 100
inc = 10
yCoordInc = 20

typedChar = 0
suggestions = ['the', 'you', 'it', 'an']
# suggestions = ['', '', '', '']
gestureToKeyMapping[10] = suggestions[0] if suggestions[0] != '' else None
gestureToKeyMapping[20] = suggestions[1] if suggestions[1] != '' else None
gestureToKeyMapping[30] = suggestions[2] if suggestions[1] != '' else None
gestureToKeyMapping[40] = suggestions[3] if suggestions[3] != '' else None

isUpdatedSuggestions = True
autocompletion = False

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
        cv2.putText(image, f'{typingUtils.getFormattedSuggestions(suggestions, 10, 10)}', (120, 85), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 0, 0), 1)

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
                            if gesture in [10, 20, 30, 40]:
                                autocompletion = True
                            else:
                                autocompletion = False
                if currentLetter != None:
                    cv2.putText(image, currentLetter, (xCoord, 110), cv2.FONT_HERSHEY_DUPLEX, 0.6, (255, 0, 0), 1)

            except Exception as e:
                if gesture == 0:
                    itr = 0
                    if currentLetter != None:
                        if currentLetter == 'ENTER':
                            last_segment = typedSentence.split(' ')[-1]
                            if last_segment.isdigit():
                                if suggestions[0] != None:
                                    currentLetter = suggestions[0]
                                    typedSentence = typedSentence[:-len(typedSentence.split(' ')[-1])] + currentLetter + ' '
                                    typedChar += len(currentLetter) - len(typedSentence.split(' ')[-1]) + 1
                            typedChar += 1
                            typedSentence = ''
                            xCoord = 100
                            typedChar = 0
                            isUpdatedSuggestions = True
                            autocompletion = False
                            suggestions = ['the', 'you', 'it', 'an']
                            gestureToKeyMapping[10] = suggestions[0] if suggestions[0] != '' else None
                            gestureToKeyMapping[20] = suggestions[1] if suggestions[1] != '' else None
                            gestureToKeyMapping[30] = suggestions[2] if suggestions[2] != '' else None
                            gestureToKeyMapping[40] = suggestions[3] if suggestions[3] != '' else None
                            itr = 0
                        elif currentLetter == 'DELETE':
                            if len(typedSentence) > 0:
                                typedChar += 1
                                isUpdatedSuggestions = False
                                typedSentence = ' '.join(typedSentence.strip().split(' ')[:-1])
                                if len(typedSentence.strip()) > 0:
                                    typedSentence += ' '
                                xCoord -= inc
                                if len(typedSentence) == 0:
                                    suggestions = ['the', 'you', 'it', 'an']
                                    gestureToKeyMapping[10] = suggestions[0] if suggestions[0] != '' else None
                                    gestureToKeyMapping[20] = suggestions[1] if suggestions[1] != '' else None
                                    gestureToKeyMapping[30] = suggestions[2] if suggestions[2] != '' else None
                                    gestureToKeyMapping[40] = suggestions[3] if suggestions[3] != '' else None
                                    isUpdatedSuggestions = True
                                if not isUpdatedSuggestions:
                                    if typedSentence[-1] == ' ':
                                        suggestions = worker(typedSentence, 'pred')
                                    else:
                                        suggestions = worker(typedSentence, 'med')
                                    gestureToKeyMapping[10] = suggestions[0] if suggestions[0] != '' else None
                                    gestureToKeyMapping[20] = suggestions[1] if suggestions[1] != '' else None
                                    gestureToKeyMapping[30] = suggestions[2] if suggestions[2] != '' else None
                                    gestureToKeyMapping[40] = suggestions[3] if suggestions[3] != '' else None
                                    isUpdatedSuggestions = True
                                
                        elif currentLetter == 'SPACE':
                            last_segment = typedSentence.split(' ')[-1]
                            if last_segment.isdigit():
                                if suggestions[0] != None:
                                    currentLetter = suggestions[0]
                                    typedSentence = typedSentence[:-len(typedSentence.split(' ')[-1])] + currentLetter + ' '
                                    typedChar += len(currentLetter) - len(typedSentence.split(' ')[-1]) + 1
                            else:
                                typedChar += 1
                                typedSentence += ' '
                            
                            xCoord += inc
                            isUpdatedSuggestions = False
                            if not isUpdatedSuggestions:
                                suggestions = worker(typedSentence, 'pred')
                                gestureToKeyMapping[10] = suggestions[0] if suggestions[0] != '' else None
                                gestureToKeyMapping[20] = suggestions[1] if suggestions[1] != '' else None
                                gestureToKeyMapping[30] = suggestions[2] if suggestions[2] != '' else None
                                gestureToKeyMapping[40] = suggestions[3] if suggestions[3] != '' else None
                                isUpdatedSuggestions = True
                        else:
                            isUpdatedSuggestions = False
                            if autocompletion:
                                if typedSentence == '':
                                    typedChar += len(currentLetter) + 1
                                    typedSentence += currentLetter + ' '
                                    xCoord += inc * (len(currentLetter) + 1)
                                elif typedSentence[-1] == ' ':
                                    typedChar += len(currentLetter) + 1
                                    typedSentence += currentLetter + ' '
                                    xCoord += inc * (len(currentLetter) + 1)
                                else:
                                    typedSentence = typedSentence[:-len(typedSentence.split(' ')[-1])] + currentLetter + ' '
                                    typedChar += len(currentLetter) - len(typedSentence.split(' ')[-1]) + 1
                                    xCoord += inc * (len(currentLetter) - len(typedSentence.split(' ')[-1]) + 1)
                            else:
                                typedChar += 1
                                typedSentence += currentLetter
                                xCoord += inc * len(currentLetter)
                            if not isUpdatedSuggestions:
                                if autocompletion:
                                    suggestions = worker(typedSentence, 'pred')
                                else:
                                    suggestions = worker(typedSentence, 'med')
                                print(suggestions)
                                gestureToKeyMapping[10] = suggestions[0] if suggestions[0] != '' else None
                                gestureToKeyMapping[20] = suggestions[1] if suggestions[1] != '' else None
                                gestureToKeyMapping[30] = suggestions[2] if suggestions[2] != '' else None
                                gestureToKeyMapping[40] = suggestions[3] if suggestions[3] != '' else None
                                isUpdatedSuggestions = True
                        currentLetter = None
                        tempLetter = None
                        autocompletion = False

                else:
                    if tempLetter != None:
                        itr += 1
                        if itr > changeThreshold:
                            tempLetter = None
                            currentLetter = None
                            itr = 0




        cv2.imshow('Test hand', image)

        if cv2.waitKey(1) == 27:
            break

cv2.destroyAllWindows()
cap.release()