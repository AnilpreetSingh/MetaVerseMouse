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
minhandHeight=270     #cameraAreaPermitted X
screenResX=1960
screenResY=1080
holdSenitivity=3
moveSenitivity=0.9
scrollSpeed=50

thScrollX,thScrollY=0.08,0.08  #thershold for scroll,3f,4f to detect direction

#NON USER CHANGEABLE VARIABLES
# numClicksPermited=3 
numClickedL=0
# opQueue=queue.Queue(3+numClicksPermited)    #queue for storing operations 
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



def opQueueAdd(opQueue,string):
    if opQueue.full():
        opQueue.get()
    opQueue.put(dictop[string])
    return opQueue
    
def returnQueueLastElm(opQueue):
    if opQueue.empty():
        return 0
    return list(opQueue.queue)[opQueue.qsize()-1]
   

def pointerMove(Xpos,Ypos,CameraResX,minhandWidth,minhandHeight,screenResX,screenResY,lastIndexX,lastIndexY,duration):

    a=CameraResX-Xpos  #restoring camera image that is horizontally flipped due to mirroring 
    a=min(a,minhandWidth)
    b=min(Ypos,minhandHeight)
    
    a,b=max(a,0),max(b,0)
    # a,b=a,b
    x=int((screenResX*a)/minhandWidth)
    y=(screenResY*b)/minhandHeight

    # print("Index finger tip coordinates: (",a,",",b,":",x,",",y,")" )
    if(abs(Xpos-lastIndexX)>moveSenitivity or abs(Ypos-lastIndexY)>moveSenitivity):
        pyautogui.moveTo(x,y, duration)
    # print(x,y)
          
          
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
    
def pointMain(mm,indxX,indxY,opQueue,lastIndexX,lastIndexY,centrePoseX,centrePoseY):
    lastElem=returnQueueLastElm(opQueue)
    # print(lastIndexX,lastIndexY)

    # return  opQueue,lastIndexX,lastIndexY  
    if not mm==[0,0,0,0,0]:
        if mm[0]==0:                                        #mm==[0,-,-,-,-]
            
            if mm==[0,1,0,0,0]:                           #move
                
                
                if lastElem == 2:#dictop["lc"]:
                        pyautogui.click(button='left')
                elif lastElem == 3:#dictop["rc"]:            
                        pyautogui.click(button='right')

                pointerMove(indxX*CameraResX,indxY*CameraResY,CameraResX,minhandWidth,minhandHeight,screenResX,screenResY,lastIndexX*CameraResX,lastIndexY*CameraResY,duration=0)
                opQueue=opQueueAdd(opQueue,"move")
                # stack.append(1)
    
            elif mm==[0,1,1,1,1]:                             #4 finger move
                
                if lastElem == dictop["4fc"]:
                        pyautogui.press('playpause')

                        
                if lastElem != dictop["4fup"] \
                    and lastElem != dictop["4fdown"]\
                        and lastElem != dictop["4fleft"]\
                            and lastElem != dictop["4fright"]\
                                and lastElem != dictop["4fc"]\
                                    and lastElem != dictop["4fmid"]: #if last operation is not 4f 
                    
                    centrePoseX,centrePoseY=indxX,indxY
                    opQueue=opQueueAdd(opQueue,"4fmid")
                    

                else:
                    dirxn=findDirxn(centrePoseX,centrePoseY,indxX,indxY)  #0=up,1=down,3=left,2=right
                    if dirxn==-1:
                        if lastElem == dictop["4fleft"]:                    
                            pyautogui.press('prevtrack')
                            # print("prevtrack")
                        elif lastElem == dictop["4fright"]:
                                pyautogui.press('nexttrack')
                                # print("nexttrack")
                        opQueue=opQueueAdd(opQueue,"4fmid")
                    elif dirxn==0:
                        pyautogui.press('volumeup')
                        opQueue=opQueueAdd(opQueue,"4fup")
                    elif dirxn==1:
                        pyautogui.press('volumedown')
                        opQueue=opQueueAdd(opQueue,"4fdown")
                    elif dirxn==3:
                        opQueue=opQueueAdd(opQueue,"4fleft")
                    elif dirxn==2:
                        opQueue=opQueueAdd(opQueue,"4fright")
            
            elif mm==[0,1,1,0,0]:                            #scrol

                if lastElem != dictop["2fup"]\
                      and lastElem != dictop["2fdown"]\
                          and lastElem != dictop["2fleft"]\
                             and lastElem != dictop["2fright"]:       #if last operation is not scroll 
                    centrePoseX,centrePoseY=indxX,indxY
                    opQueue=opQueueAdd(opQueue,"2fup")
                else:
                    dirxn=findDirxn(centrePoseX,centrePoseY,indxX,indxY)  #0=up,1=down,3=left,2=right
                    if dirxn==-1:
                        pass 
                    elif dirxn==0:
                        pyautogui.scroll(scrollSpeed)
                        opQueue=opQueueAdd(opQueue,"2fup")
                    elif dirxn==1:
                        pyautogui.scroll(-scrollSpeed)
                        opQueue=opQueueAdd(opQueue,"2fdown")
                    elif dirxn==3:
                        pyautogui.hscroll(-scrollSpeed)
                        opQueue=opQueueAdd(opQueue,"2fleft")
                    elif dirxn==2:
                        pyautogui.hscroll(scrollSpeed)
                        opQueue=opQueueAdd(opQueue,"2fright")
         
            elif mm==[0,1,1,1,0]:                             #3 finger move
                
                if lastElem == dictop["3fc"]:
                        pyautogui.press('win')
                        
                if lastElem != dictop["3fup"] \
                    and lastElem != dictop["3fdown"]\
                        and lastElem != dictop["3fleft"]\
                            and lastElem != dictop["3fright"]\
                                and lastElem != dictop["3fc"]:       #if last operation is not 3f 
                    centrePoseX,centrePoseY=indxX,indxY
                    opQueue=opQueueAdd(opQueue,"3fup")
                else:
                    dirxn=findDirxn(centrePoseX,centrePoseY,indxX,indxY)  #0=up,1=down,3=left,2=right
                    if dirxn==-1:
                        if lastElem == dictop["3fleft"]:                    
                            pyautogui.hotkey('alt', 'tab')
                            # print("alt tab")
                        elif lastElem == dictop["3fright"]:                   
                            pyautogui.hotkey('alt', 'shift','tab')
                            # print("alt shift tab")
                        opQueue=opQueueAdd(opQueue,"4fmid")
                    elif dirxn==0:
                        pyautogui.press('pgup')
                        opQueue=opQueueAdd(opQueue,"3fup")
                    elif dirxn==1:
                        pyautogui.press('pgdn')
                        opQueue=opQueueAdd(opQueue,"3fdown")
                    elif dirxn==3:
                        # pyautogui.press('home')
                        opQueue=opQueueAdd(opQueue,"3fleft")
                    elif dirxn==2:
                        # pyautogui.press('end')
                        opQueue=opQueueAdd(opQueue,"3fright")


        else:  
            
            if mm==[1,1,0,0,0]:                          #left click
                opQueue=opQueueAdd(opQueue,"lc")
            
            elif mm==[1,1,0,0,1]:                          #right click
                opQueue=opQueueAdd(opQueue,"rc")  

            elif mm==[1,1,1,1,1]:                            #4 finger click
                opQueue=opQueueAdd(opQueue,"4fc")                                          

            elif mm==[1,1,1,1,0]:                          #3 finger click
                opQueue=opQueueAdd(opQueue,"3fc")

            elif mm==[1,1,1,0,0]:                          #scroll click
                opQueue=opQueueAdd(opQueue,"2fc")  

    
    else:
        # numClickedL=0                
        opQueue=opQueueAdd(opQueue,"none")
            
    return opQueue,indxX,indxY,centrePoseX,centrePoseY
                        
  
    
