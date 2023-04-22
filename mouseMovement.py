import pyautogui
import queue


#User changeable variables
numClickedL=0
numClickedR=0
numClicksPermited=3 
pyautogui.FAILSAFE = False
CameraResX=640  
CameraResY=480 
minhandWidth=520      #cameraAreaPermitted X
minhandHeight=300     #cameraAreaPermitted X
screenResX=1960
screenResY=1080
holdSenitivity=3
scrollSpeed=50

thScrollX,thScrollY=0.1,0.1  #thershold for scroll,3f,4f to detect direction

#NON USER CHANGEABLE VARIABLES
numClicksPermited=3 
numClickedL=0
opQueue=queue.Queue(3+numClicksPermited)    #queue for storing operations 
dictop={                                #dictionary of operations
 'none': 0,
 'move': 1,
 'lc': 2,
 'rc': 3,
 'dblc': 4,
 '2fup': 5,
 '2fdown': 6,
 '2fleft': 7,
 '2fright': 8,
 '3fup': 9,
 '3fdown': 10,
 '3fleft': 11,
 '3fright': 12,
 '4fup': 13,
 '4fdown': 14,
 '4fleft': 15,
 '4fright': 16,
 '2fc': 17,
 '3fc': 18,
 '4fc':19,
 '4fmid':20
}

scrollX,scrollY=0,0
threefX,threefY=0,0
fourfX,fourfY=0,0


def setglobalvars(cameraresX,cameraresY):
    global CameraResX,CameraResY
    CameraResX=cameraresX
    CameraResY=cameraresY


def opQueueAdd(string):
    global opQueue
    if opQueue.full():
        opQueue.get()
    opQueue.put(dictop[string])
    
def returnQueueLastElm():
    global opQueue
    if opQueue.empty():
        return 0
    return list(opQueue.queue)[opQueue.qsize()-1]
   
   
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

def pointerMove(Xpos,Ypos,CameraResX,minhandWidth,minhandHeight,screenResX,screenResY,duration):

    a=CameraResX-Xpos  #restoring camera image that is horizontally flipped due to mirroring 
    a=min(a,minhandWidth)
    b=min(Ypos,minhandHeight)
    
    a,b=max(a,0),max(b,0)
    # a,b=a,b
    x=(screenResX*a)/minhandWidth
    y=(screenResY*b)/minhandHeight

    x=int(min(x,screenResX))  # for precatutions only actual value doesn't exceed screen res in actual conditions
    y=int(min(y,screenResY))
    # print("Index finger tip coordinates: (",a,",",b,":",x,",",y,")" )
    pyautogui.moveTo(x,y, duration)

    # dict1={ "X1":a,"Y1":b, "X2"=x, "Y2"=y}
    # out_file = open("myfile.json", "w") 
    # json.dump(dict1, out_file, indent = 6) 
    # out_file.close()
    print (a,b,x,y)
          
          
def findDirxn(x1,y1,x2,y2):    
    if abs(x1-x2)<thScrollX and abs(y1-y2)<thScrollY:
        return -1
    elif abs(x1-x2)<thScrollX and y1-y2>thScrollY:
        return 0
    elif abs(x1-x2)<thScrollX and y2-y1>thScrollY:
        return 1
    elif abs(y1-y2)<thScrollY and x1-x2>thScrollX:
        return 2
    elif abs(y1-y2)<thScrollY and x2-x1>thScrollX:
        return 3
    
def pointMain(landmark_matrix,handType):
    mm=detectfingers(landmark_matrix,handType) #mouse matrix
    global numClickedL

    if mm==[0,0,0,0,0]:
        # stack.append(0)
        numClickedL=0
                
        opQueueAdd("none")

    else:
        if mm[0]==1:
            
            if mm==[1,1,1,1,1]:                            #4 finger click
                
                #toggle play pause
                opQueueAdd("4fc")                                          

            elif mm==[1,1,1,1,0]:                          #3 finger click
                opQueueAdd("3fc")

            elif mm==[1,1,1,0,0]:                          #scroll click
                #Some operation
                opQueueAdd("2fc")  

            elif mm==[1,1,0,0,1]:                          #right click
                opQueueAdd("rc")  

            elif mm==[1,1,0,0,0]:                          #left click
                    opQueueAdd("lc")


        else:     
                                                    #mm==[0,-,-,-,-]
            if mm==[0,1,1,1,1]:                             #4 finger move
                
                if returnQueueLastElm() == dictop["4fc"]:
                        pyautogui.press('playpause')

                        
                if returnQueueLastElm() != dictop["4fup"] \
                    and returnQueueLastElm() != dictop["4fdown"]\
                          and returnQueueLastElm() != dictop["4fleft"]\
                              and returnQueueLastElm() != dictop["4fright"]\
                              and returnQueueLastElm() != dictop["4fmid"]: #if last operation is not 4f 
                    global fourfX,fourfY
                    fourfX,fourfY=landmark_matrix[8][0],landmark_matrix[8][1]
                    opQueueAdd("4fmid")
                    

                else:
                    dirxn=findDirxn(fourfX,fourfY,landmark_matrix[8][0],landmark_matrix[8][1])  #0=up,1=down,3=left,2=right
                    if dirxn==-1:
                        if returnQueueLastElm() == dictop["4fleft"]:                    
                            pyautogui.press('prevtrack')
                            # print("prevtrack")
                        elif returnQueueLastElm() == dictop["4fright"]:
                                pyautogui.press('nexttrack')
                                # print("nexttrack")
                        opQueueAdd("4fmid")
                    elif dirxn==0:
                        pyautogui.press('volumeup')
                        opQueueAdd("4fup")
                    elif dirxn==1:
                        pyautogui.press('volumedown')
                        opQueueAdd("4fdown")
                    elif dirxn==3:
                        opQueueAdd("4fleft")
                    elif dirxn==2:
                        opQueueAdd("4fright")

            if mm==[0,1,1,1,0]:                             #3 finger move
                
                if returnQueueLastElm() == dictop["3fc"]:
                        pyautogui.press('win')
                if returnQueueLastElm() != dictop["3fup"] \
                    and returnQueueLastElm() != dictop["3fdown"]\
                          and returnQueueLastElm() != dictop["3fleft"]\
                              and returnQueueLastElm() != dictop["3fright"]:       #if last operation is not 3f 
                    global threefX,threefY
                    threefX,threefY=landmark_matrix[8][0],landmark_matrix[8][1]
                    opQueueAdd("3fup")
                else:
                    dirxn=findDirxn(threefX,threefY,landmark_matrix[8][0],landmark_matrix[8][1])  #0=up,1=down,3=left,2=right
                    if dirxn==-1:
                        pass
                    elif dirxn==0:
                        pyautogui.press('pgup')
                        opQueueAdd("3fup")
                    elif dirxn==1:
                        pyautogui.press('pgdn')
                        opQueueAdd("3fdown")
                    elif dirxn==3:
                        pyautogui.press('home')
                        opQueueAdd("3fleft")
                    elif dirxn==2:
                        pyautogui.press('end')
                        opQueueAdd("3fright")

            elif mm==[0,1,1,0,0]:                            #scrol


                if returnQueueLastElm() != dictop["2fup"]\
                      and returnQueueLastElm() != dictop["2fdown"]\
                          and returnQueueLastElm() != dictop["2fleft"]\
                             and returnQueueLastElm() != dictop["2fright"]:       #if last operation is not scroll 
                    global scrollX,scrollY
                    scrollX,scrollY=landmark_matrix[8][0],landmark_matrix[8][1]
                    opQueueAdd("2fup")
                else:
                    dirxn=findDirxn(scrollX,scrollY,landmark_matrix[8][0],landmark_matrix[8][1])  #0=up,1=down,3=left,2=right
                    if dirxn==-1:
                        pass 
                    elif dirxn==0:
                        pyautogui.scroll(scrollSpeed)
                        opQueueAdd("2fup")
                    elif dirxn==1:
                        pyautogui.scroll(-scrollSpeed)
                        opQueueAdd("2fdown")
                    elif dirxn==3:
                        pyautogui.hscroll(-scrollSpeed)
                        opQueueAdd("2fleft")
                    elif dirxn==2:
                        pyautogui.hscroll(scrollSpeed)
                        opQueueAdd("2fright")

            elif mm==[0,1,0,0,0]:                           #move
                
                
                if returnQueueLastElm() == dictop["rc"]:            
                        pyautogui.click(button='right')
                elif returnQueueLastElm() == dictop["lc"]:
                        pyautogui.click(button='left')

                pointerMove(landmark_matrix[8][0]*CameraResX,landmark_matrix[8][1]*CameraResY,CameraResX,minhandWidth,minhandHeight,screenResX,screenResY,duration=0)
                opQueueAdd("move")
                # stack.append(1)
            
                
                        
  
    
