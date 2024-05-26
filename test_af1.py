from imutils.video import VideoStream                             
import time                             
import cv2 
import RPi.GPIO as GPIO
from RpiMotorLib import RpiMotorLib
import threading
import numpy as np

start = time.time()

GPIO_pins = (16, 12, 6) 
direction = 21      
step = 20
global x
global re
x = 0
mymotortest = RpiMotorLib.A4988Nema(direction, step, GPIO_pins, "A4988")

def motor():
    mymotortest.motor_go(True, "Full", 1000, 0.0076, False, 0.05)  
    print("time taken for motor",time.time()-start)

def canny(img):
    canny_var = cv2.Canny(img,100,200).var()
    return canny_var

def blurness():                     
    print("[INFO] starting canny...")
    lap_val=[]
    pos_val=[]
    i=0
    while True:
        if i<1000:
            frame = vs.read()                               
            crop = frame[70:460, 110:490]
            gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
            canny_var = canny(gray)
            lap_val.append(canny_var)
            pos_val.append(i) 
            i=i+1
        else:                              
            max_lap = lap_val.index(max(lap_val))              
            Max = lap_val[max_lap]                                                       
            break
    print("time taken for canny",time.time()-start, max_lap, Max)
    mymotortest.motor_go(False, "Full", 1000-max_lap, 0.0009, False, 0.05)
    print("Total time taken",time.time()-start)
    global x
    x = max_lap
    
    file = open('steps1.txt',"w")
    file.write(str(x))
    file.close
    
def preview():
    while True:
        global re
        frame = vs.read()                               
        crop = frame[70:460, 110:490]
        gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
        canny_var1 = canny(gray)
        text = "Bluriness {:.4f}"
        
        text = text.format(canny_var1)                       
        cv2.putText(crop, text, (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2) 
        cv2.imshow("Frame", crop)
       
        key = cv2.waitKey(1) & 0xFF                     
        if key == ord("q"):
            
            break
    cv2.destroyAllWindows()                             
    vs.stop()

if __name__=="__main__":
    try:
        global re
        file = open("steps1.txt","r")
        re = int(file.read())
        file.close()        
    except:
        file = open("steps1.txt","w+")
        file.write("0")
        file.close()
        re =0
    if (re>1 or re ==0):
        mymotortest.motor_go(False, "Full", re, 0.0009, False, 0.05)
        
    t1 = threading.Thread(target = motor)
    t2 = threading.Thread(target = blurness)
    t3 = threading.Thread(target = preview)
    vs = VideoStream(src=0).start()
    t1.start()
    t2.start()
    t3.start()
    t1.join()
    t2.join()
    t3.join()