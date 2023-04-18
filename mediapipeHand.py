import cv2
import mediapipe as mp
import mouseMovement as mm
import time
import imutils
import numpy as np
#--------------------------------------------------------------------------------------------------------------------------


def detectHands(image, hands, draw=True,flipType=True):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) #Mediapipe works in RGB
    image = imutils.resize(image, width=900, height=900)
    results = hands.process(image) # using the hands object to process the image
    image.flags.writeable = True


    for1=0
    for2=0
    landmark_matrix=[]
    handTypeLoR="Right"
    if results.multi_hand_landmarks:
        no_of_hands=0    # why is this here?
        for handType, handLms in zip(results.multi_handedness, results.multi_hand_landmarks):

            if flipType:
                    if handType.classification[0].label == "Right":
                        handTypeLoR = "Left"
                    else:
                        handTypeLoR = "Right"
            else:
                    handTypeLoR = handType.classification[0].label

            for id, lm in enumerate(handLms.landmark):
                    px, py, pz = lm.x,lm.y,lm.z
                    landmark_matrix.append([px, py, pz])
            if draw:
                image=draw_landmarks(image,handLms)

    return landmark_matrix,handTypeLoR,image

def draw_landmarks(image,hand_landmarks):
    mp_draw = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
    
    mp_hands = mp.solutions.hands
    mp_draw.draw_landmarks(image = image, landmark_list = hand_landmarks,connections = mp_hands.HAND_CONNECTIONS)
    return image


def main():
    cap=cv2.VideoCapture(0)
    
    mp_hands = mp.solutions.hands
    hands= mp_hands.Hands(
        # model_complexity=0,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
        # min_hand_presence_confidence=0.3,
        max_num_hands=1,
        # static_image_mode=False
    )

    # mm_variables=mm.vars()


    #timekeeping vars
    total_time=0
    total_itrs=0
    mm_module_time=0
    mm_prev_time=0

    while cap.isOpened(): 

        start_time = time.time()

        success, image=cap.read() 
        if not success:
            continue

        landmark_matrix,handType,image=detectHands(image,hands,draw=True)
        # print length and size of list landmark_matriz 
        if landmark_matrix:
             
            mm_start_time = time.time()

            # functions that operates the mouse 

            fingers_matrix=mm.pointMain(landmark_matrix,handType)

            mm_end_time = time.time()
            mm_module_time += mm_end_time - mm_start_time

        
        
            # cv2.putText(image,str(int(fingers_matrix)) , (10, 70), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,0), 2)#str(''.join(map(str, fingers_matrix)))
            mm_prev_time=mm_start_time

        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))

        end_time = time.time()
        total_time += end_time - start_time
        total_itrs += 1
        if (cv2.waitKey(5) & 0xFF == 27):# or returnfrommm==-1 :
            break

    cap.release()
    cv2.destroyAllWindows()
    print("Average FPS: ", total_itrs / total_time)
    # # print("Average time per frame: ", total_time/total_itrs,"ns")
    print("Time taken by mouseMovement module : ",(mm_module_time/total_time)*100,"%")
    print("Time taken by MediaPipe detection : ",100-(mm_module_time/total_time)*100,"%")

if __name__ == "__main__":
    main()