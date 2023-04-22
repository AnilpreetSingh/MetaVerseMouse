import cv2
import mediapipe as mp
from mouseMovement import pointMain
import time
from  imutils import resize
import queue
#--------------------------------------------------------------------------------------------------------------------------
   
def detectfingers(landmark_matrix,myHandType):
    tipIds = [4, 8, 12, 16, 20]
    if landmark_matrix:
        fingers = []
        # Thumb
        if myHandType == "Right":
            if landmark_matrix[tipIds[0]][0] > landmark_matrix[tipIds[0] - 1][0]:
                fingers.append(1)
            else:
                fingers.append(0)
        else:
            if landmark_matrix[tipIds[0]][0] < landmark_matrix[tipIds[0] - 1][0]:
                fingers.append(1)
            else:
                fingers.append(0)

        # 4 Fingers
        for id in range(1, 5):
            if landmark_matrix[tipIds[id]][1] < landmark_matrix[tipIds[id] - 2][1]:
                fingers.append(1)
            else:
                fingers.append(0)
    return fingers

def detectHands(image, hands, draw=True,flipType=True):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) #Mediapipe works in RGB
    image = resize(image, width=900, height=900)
    results = hands.process(image) # using the hands object to process the image
    image.flags.writeable = True


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

  
    # mm.setglobalvars(cameraresX,cameraresY)
    cap=cv2.VideoCapture(0)
    # cap.set(cv2.CAP_PROP_FRAME_WIDTH, cameraresX)
    # cap.set(cv2.CAP_PROP_FRAME_HEIGHT, cameraresY)
    
    mp_hands = mp.solutions.hands
    hands= mp_hands.Hands(
        model_complexity=1,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.75,

        max_num_hands=1,
        # static_image_mode=False
    )

    # mm_variables=mm.vars()


    #timekeeping vars
    total_time=0
    total_itrs=0
    mm_module_time=0
    mm_prev_time=0

    numClicksPermited=3 
    opQueue=queue.Queue(3+numClicksPermited)  
    lastIndexX,lastIndexY=0,0   
    centrePoseX,centrePoseY=0,0

    while cap.isOpened(): 

        start_time = time.time()

        success, image=cap.read() 
        # print(image.shape)
        if not success:
            continue

        landmark_matrix,handType,image=detectHands(image,hands,draw=True)
        # print length and size of list landmark_matriz 
        if landmark_matrix:
             
            mm_start_time = time.time()

            # functions that operates the mouse 

            fingers_matrix=detectfingers(landmark_matrix,handType)
            opQueue, lastIndexX,lastIndexY,centrePoseX,centrePoseY =pointMain(fingers_matrix,landmark_matrix[8][0],landmark_matrix[8][1],opQueue, lastIndexX,lastIndexY,centrePoseX,centrePoseY)


            mm_end_time = time.time()
            mm_module_time += mm_end_time - mm_start_time


            mm_prev_time=mm_start_time

        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        cv2.imshow('MediaPipe Hands', cv2.flip(resize(image, width=500, height=500), 1))

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