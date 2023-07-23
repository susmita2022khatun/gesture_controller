import cv2
import pyautogui
import mediapipe as mp
import webbrowser
import sys
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
finger_Coord = [(8, 6), (12, 10), (16, 14), (20, 18)]
thumb_Coord = (4,2)
alt_opened = False
thisPC_opened = False
browser_opened = False


webcam = cv2.VideoCapture(0)
while True:
    success, img = webcam.read()
    
    #model
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = mp_hands.Hands(max_num_hands = 2, min_detection_confidence= 0.7, min_tracking_confidence = 0.5).process(img)
    multiLandMarks = results.multi_hand_landmarks
    if multiLandMarks:
        handList = []
        for handLms in multiLandMarks:
            mp_drawing.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS)
            for idx, lm in enumerate(handLms.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                handList.append((cx, cy))
            for point in handList:
                cv2.circle(img, point, 10, (255, 255, 0), cv2.FILLED)
            upCount = 0
        for coordinate in finger_Coord:
            if handList[coordinate[0]][1] < handList[coordinate[1]][1]:
                upCount += 1
        if handList[thumb_Coord[0]][0] > handList[thumb_Coord[1]][0]:
            upCount += 1
        cv2.putText(img, str(upCount), (150,150), cv2.FONT_HERSHEY_PLAIN, 12, (0,255,0), 12)
        
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        cv2.imshow('frame', img)
    
        #decision channel
        if upCount > 0:
            if not thisPC_opened and not browser_opened and not alt_opened:
                if  upCount == 1:
                    print("Opening My Computer...")
                    pyautogui.hotkey('win', 'e')
                    thisPC_opened = True


                elif  upCount == 2:
                    print("opening web browser...")
                    webbrowser.open('https://www.google.co.in')
                    browser_opened = True

                elif  upCount == 3:
                    pass


                elif  upCount == 4:
                    print("Exiting...")
                    sys.exit()


            elif thisPC_opened and not browser_opened:
                if  upCount == 1:
                    pyautogui.press('right')

                elif  upCount == 2:
                    pyautogui.press('space')

                elif upCount == 3:
                    pyautogui.press('enter')

                elif  upCount == 4:
                    pyautogui.hotkey('alt', 'f4')
                    thisPC_opened = False


            elif not thisPC_opened and browser_opened:
                if  upCount == 1:
                    pyautogui.hotkey('ctrl', 't')

                elif upCount == 2:
                    pyautogui.typewrite('https://www.youtube.com/')
                    pyautogui.press('enter')

                elif  upCount == 3:
                    pyautogui.typewrite('https://www.google.com/gmail')
                    pyautogui.press('enter')

                elif  upCount == 4:
                    pyautogui.hotkey('alt', 'f4')
                    browser_opened = False
     
     
        
    
    if cv2.waitKey(5) & 0xFF == ord("q"):
        break
webcam.release()
cv2.destroyWindow('frame')