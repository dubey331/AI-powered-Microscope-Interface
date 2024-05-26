import tkinter as tk
import customtkinter
import cv2
from datetime import datetime
from PIL import Image, ImageTk
from tkinter import messagebox, filedialog
from imutils.video import VideoStream

import RPi.GPIO as GPIO
from RpiMotorLib import RpiMotorLib
import threading
import time 

GPIO_pins = (16, 12, 6) 
direction = 20      
step = 21

global re

global start
start = time.time()

mymotortest = RpiMotorLib.A4988Nema(direction, step, GPIO_pins, "A4988")

customtkinter.set_appearance_mode("Dark")  
customtkinter.set_default_color_theme("dark-blue")
customtkinter.deactivate_automatic_dpi_awareness()

def window():
    root.switch_1 = customtkinter.CTkSwitch(master=root, text="Automatic", command=enable)
    root.switch_1.grid(row=3, column=1, columnspan=1, pady=10, padx=10)
    
    root.button_3 = customtkinter.CTkButton(master=root, text="Autofocus", state=tk.DISABLED, command=thread)
    root.button_3.grid(row=4, column=1, pady=10, padx=10)
    
    root.feedlabel = customtkinter.CTkLabel(root, text="Camera Feed")
    root.feedlabel.grid(row=1, column=1, padx=10, pady=5, columnspan=2)
    
    root.cameraLabel = customtkinter.CTkLabel(root, borderwidth=2, relief="groove")
    root.cameraLabel.grid(row=2, column=1, padx=10, pady=5, columnspan=2)
    
    #root.feedlabel1 = customtkinter.CTkLabel(root, text="autofocus")
    #root.feedlabel1.grid(row=1, column=3, padx=10, pady=5, columnspan=2)
    
    #root.cameraLabel1 = customtkinter.CTkLabel(root, borderwidth=2, relief="groove")
    #root.cameraLabel1.grid(row=2, column=3, padx=10, pady=5, columnspan=2)

    ShowFeed()
    #ShowFeed2()
    
def thread():
    t1 = threading.Thread(target=motor)
    t2 = threading.Thread(target=blur)
    #t3 = threading.Thread(target=ShowFeed2)
    
    if root.switch_1.get():
        try:
            global re
            file = open("steps1.txt","r")
            re = int(file.read())
            #print("try",re)
            file.close()
        except:
            file = open("steps1.txt","w")
            file.write("0")
            file.close()
            re = 0
            #print("except",re)
        if (re>1 or re ==0):
            mymotortest.motor_go(False, "Full", re, 0.0009, False, 0.05)
            print("return")
            
        t1.start()
        t2.start()
        #t3.start()
        t1.join()
        t2.join()
        #t3.join()

def canny(img):
    canny_var = cv2.Canny(img,100,200).var()
    return canny_var

def motor():
    global start
    start1 = time.time()
    mymotortest.motor_go(True, "Full", 1000, 0.0076, False, 0.05)
    print(time.time()-start)
    print("motor time",time.time()-start1)

def blur():
    global start
    start2 = time.time()
    lap_val=[]
    pos_val=[]
    i=0
    while True:
        if i<1000:
            frame = root.cap.read()                               
            #crop = frame[70:460, 110:490]
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            canny_var = canny(gray)
            #print(i,canny_var)
            lap_val.append(canny_var)
            pos_val.append(i)
            i=i+1
        else:
            Max_lap = lap_val.index(max(lap_val))
            break
    print(time.time()-start)
    print("canny time",time.time()-start2,Max_lap)
    mymotortest.motor_go(False, "Full", 1000-Max_lap, 0.0009, False, 0.05)
    
    x = Max_lap
    file = open("steps1.txt","w")
    file.write(str(x))
    file.close()

'''def ShowFeed2():
    frame = root.cap.read()
    #frame = cv2.flip(frame, 1)
    blur = canny(frame)
    cv2.putText(frame, datetime.now().strftime('%d/%m/%Y %H:%M:%S')+str("  ")+str("blurness")+str("  ")+str(int(blur)), (20,30), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0,255,255))
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    videoImg = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image = videoImg)
    root.cameraLabel1.configure(image=imgtk)
    root.cameraLabel1.imgtk = imgtk
    root.cameraLabel1.after(10, ShowFeed2)'''

def ShowFeed():
    frame = root.cap.read()
    #frame = cv2.flip(frame, 1)
    blur = canny(frame)
    cv2.putText(frame, datetime.now().strftime('%d/%m/%Y %H:%M:%S')+str("  ")+str("blurness")+str("  ")+str(int(blur)), (20,30), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0,255,255))
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    videoImg = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image = videoImg)
    root.cameraLabel.configure(image=imgtk)
    root.cameraLabel.imgtk = imgtk
    root.cameraLabel.after(10, ShowFeed)
        
def enable():
    if root.switch_1.get():
        root.button_3.configure(state=tk.NORMAL)
    else:
        root.button_3.configure(state=tk.DISABLED)

root = customtkinter.CTk() 

width1 = root.winfo_screenwidth()
height1 = root.winfo_screenheight()

root.cap = VideoStream(src=0).start()

root.var = customtkinter.StringVar(value="Normal")
destPath = tk.StringVar()
imagePath = tk.StringVar()

root.title("Microscope")
root.geometry(f'{width1}x{height1}')
root.resizable(True, True)

window()
root.mainloop()