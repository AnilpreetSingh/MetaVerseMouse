import cv2
import mediapipe as mp
import numpy as np
import time
import imutils

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

#--------------------------------------------------------------------------------------------------------------------------

def poseUp(landmark_matrix):
    # print("Landmark Matrix: ", landmark_matrix)
    # print("Rs",landmark_matrix[12][1])
    # print("Rh",landmark_matrix[24][1])
    # print("Rk",landmark_matrix[26][1])
    if landmark_matrix[12][1] < landmark_matrix[24][1] and landmark_matrix[24][1] < landmark_matrix[26][1]:
        return 1
    else:
        return 0



def detectPose(image, pose, draw=True,flipType=True):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) #Mediapipe works in RGB
    image = imutils.resize(image, width=900, height=900)
    results = pose.process(image) # using the hands object to process the image
    image.flags.writeable = True

    landmark_matrix=[]
    if results.pose_landmarks:
        for id, lm in enumerate(results.pose_landmarks.landmark):
                px, py, pz = lm.x,lm.y,lm.z
                landmark_matrix.append([px, py, pz])
        if draw:
                mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                            mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
                            mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2) 
                                ) 

    return landmark_matrix,image

def draw_landmarks(image,hand_landmarks):
    mp_draw = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
    
    mp_hands = mp.solutions.hands
    mp_draw.draw_landmarks(image = image, landmark_list = hand_landmarks,connections = mp_hands.HAND_CONNECTIONS)
    return image


def alarmControl():
    cap=cv2.VideoCapture(0)  


    pose= mp_pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) 


    #timekeeping vars
    total_time=0
    total_itrs=0
    mm_module_time=0
    mm_prev_time=0
    isStandingcounter=0

    while cap.isOpened(): 

        start_time = time.time()

        success, image=cap.read() 
        if not success:
            continue

        landmark_matrix,image=detectPose(image,pose,draw=True)
        # print length and size of list landmark_matriz 
        if landmark_matrix:
             
            mm_start_time = time.time()

            # functions that operates the mouse 

            standing=poseUp(landmark_matrix)
            standingText="Standing" if standing else "Not Standing"
            if standing==0:
                    playAlarm()
                    print("Still sleeping")
                    isStandingcounter=0
            else:
                isStandingcounter+=1
                if isStandingcounter>10:
                    print("Alarm off at ",time.localtime(time.time()).tm_hour,":",time.localtime(time.time()).tm_min)
                    exit(0)


            mm_end_time = time.time()
            mm_module_time += mm_end_time - mm_start_time

        
            # cv2.flip(image, 1)
            cv2.putText(image, str(standingText), (10, 70), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,0), 2)
            mm_prev_time=mm_start_time

        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        cv2.imshow('Current Pose', image)

        end_time = time.time()
        total_time += end_time - start_time
        total_itrs += 1
        if (cv2.waitKey(5) & 0xFF == 27):# or returnfrommm==-1 :
            break
    pose.close()
    cap.release()
    cv2.destroyAllWindows()
    print("Average FPS: ", total_itrs / total_time)
    return

def playAlarm():
    #play windows beep
    # winsound.Beep(2500, 1000)
    print("Alarm ringing ")
    print("............")
    return

def main():
    programStartTime = time.localtime(time.time())
    while True:
        #  playAlarm()
        localtime = time.localtime(time.time())
        if localtime.tm_hour == programStartTime.tm_hour and localtime.tm_min == programStartTime.tm_min and localtime.tm_sec == programStartTime.tm_sec+5:
          print("Alarm turned on at ",time.localtime(time.time()).tm_hour,":",time.localtime(time.time()).tm_min)
          alarmControl() 

if __name__ == "__main__":
    main()