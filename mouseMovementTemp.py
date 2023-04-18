import pyautogui

numClickedL=0
numClickedR=0
numClicksPermited=3 
pyautogui.FAILSAFE = False
CameraResX=640   
minhandWidth=520      #cameraAreaPermitted X
minhandHeight=300  #cameraAreaPermitted X
screenResX=1960
screenResY=1080


def moveCursor(a,b,duration=0):
    a=CameraResX-a  #restoring camera image that is horizontally flipped due to mirroring 
    a=min(a,minhandWidth)
    b=min(b,minhandHeight)
    
    a,b=max(a,0),max(b,0)

    x=screenResX*(a/minhandWidth)
    y=screenResY*(b/minhandHeight)

    x=int(min(x,screenResX))  # for precatutions only actual value doesn't exceed screen res in actual conditions
    y=int(min(y,screenResY))
    # print("Index finger tip coordinates: (",a,",",b,":",x,",",y,")" )
    pyautogui.moveTo(x,y, duration)
    return 
def showZ(z):
       print(z)
       return

def click_protocol(landmark_coords):
    L=0
    R=0
    global numClickedL
    global numClickedR
#the number of times both left click and right click can be clicked simultaneously that will count as a single click
    if landmark_coords[4][0]>landmark_coords[3][0]:
        # print("Left click")
        # print("...l")
        L=1 
        numClickedL+=1
    if landmark_coords[19][1]>landmark_coords[20][1] and L==1 :
        # print("Right c'   lick")
        # print("...r"/.,)
        R=1     
        L=0  

        numClickedR+=1

    #actual clicking 
    if R==1 and numClickedR==1 :
                pyautogui.click(button='right')
    elif R==0 and L==1 and numClickedL==1 : 
                pyautogui.click(button='left')

    numClickedR=0 if numClickedR==numClicksPermited else numClickedR #resetting the numClicked variable to not excedding numClicksPermited
    numClickedL=0 if numClickedL==numClicksPermited else numClickedL #resetting the numClicked variable to not excedding numClicksPermited

    return L,R


