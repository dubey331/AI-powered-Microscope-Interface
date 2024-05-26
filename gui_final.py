import tkinter as tk
import customtkinter
import cv2
from datetime import datetime
from PIL import Image, ImageTk
import imutils
from tkinter import messagebox, filedialog
import numpy as np
import threading 
import serial 
import time
from imutils.video import VideoStream
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

import RPi.GPIO as GPIO
from RpiMotorLib import RpiMotorLib

GPIO_pins = (16, 12, 6) 
direction = 21
step = 20

global re

global start
start = time.time()

mymotortest = RpiMotorLib.A4988Nema(direction, step, GPIO_pins, "A4988")

customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")
customtkinter.deactivate_automatic_dpi_awareness()

global x
x="Normal"

s = serial.Serial(port='/dev/ttyACM0', baudrate=115200)
s.write("\r\n\r\n".encode())
time.sleep(2)
s.flushInput()

global Stop 
Stop = 0

y_co = 0.1
x_co = 0.1
feed_ba = 50

y_coo = 0
x_coo = 0

def up():
    global y_coo
    global x_coo
    y_coo = round(y_coo + float(y_co),2)
    l = 'G21G90G1X'+str(x_coo)+'Y'+str(y_coo)+'F'+str(feed_ba)+'\n'
    s.write(l.encode())
    return l 

def down():
    global y_coo
    global x_coo
    y_coo = round(y_coo - float(y_co),2)
    l = 'G21G90G1X'+str(x_coo)+'Y'+str(y_coo)+'F'+str(feed_ba)+'\n'
    s.write(l.encode())
    return l

def left():
    global y_coo
    global x_coo
    x_coo = round(x_coo - float(x_co),2)
    l = 'G21G90G1X'+str(x_coo)+'Y'+str(y_coo)+'F'+str(feed_ba)+'\n'
    s.write(l.encode())
    return l

def right():
    global y_coo
    global x_coo
    x_coo = round(x_coo + float(y_co),2)
    l = 'G21G90G1X'+str(x_coo)+'Y'+str(y_coo)+'F'+str(feed_ba)+'\n'
    s.write(l.encode())
    return l

def home():
    l='G28 X0 Y0'+'\n'
    s.write(l.encode())
    global y_coo
    global x_coo
    x_coo = 0 
    y_coo = 0
    return l

def stop():
    l='!'+'\n'
    s.write(l.encode())
    stop = 1

def resume():
    l='~'+'\n'
    s.write(l.encode())
    stop = 0

def window():

    root.frame_right = customtkinter.CTkFrame(master=root, corner_radius=1, width= 50, fg_color="#0A0A0A")
    root.frame_right.pack(side="right", fill="both")

    root.frame_left = customtkinter.CTkFrame(master=root, corner_radius=1, width= 200, fg_color="#0A0A0A")
    root.frame_left.pack(side="left", fill="both")

    root.frame_center = customtkinter.CTkFrame(master=root, corner_radius=1, fg_color="#0A0A0A")
    root.frame_center.pack(fill="both",expand=True)
    #center
    root.cameraLabel = tk.Label(root.frame_center, bg="black", borderwidth=3, relief="groove")
    root.cameraLabel.pack(fill="both", expand=True, pady=40)

    #left
    root.logo = ImageTk.PhotoImage(Image.open("imead.png").resize((180,120),Image.ANTIALIAS))
    root.Label = customtkinter.CTkLabel(root.frame_left, text="", image=root.logo, bg="#0A0A0A",fg ="#808080",text_font=("Helvetica 20 bold",40))
    root.Label.grid(row=0, column=1, pady=10, padx=10)

    #root.Label = tk.Label(root.frame_left, text="",bg="#0A0A0A")
    #root.Label.grid(row=1, column=1, pady=10, padx=10)

    root.Label = customtkinter.CTkLabel(root.frame_left, text="Filters ",bg="#0A0A0A",fg ="#ffffff",text_font=("Helvetica 20 bold",15))
    root.Label.grid(row=2, column=1, pady=10, padx=10)

    root.filter = customtkinter.CTkOptionMenu(master = root.frame_left, values=["Normal","Red","Green","Blue","Segmentation"], variable=root.var, text_color ="#808080",fg_color="#0A0A0A",text_font=("Helvetica 20 bold",10), command=filter_change)
    root.filter.grid(row=3, column=1, pady=10, padx=10)

    root.view_3=ImageTk.PhotoImage(Image.open("stich.png").resize((30, 30),Image.ANTIALIAS))
    root.stick = customtkinter.CTkButton(master=root.frame_left,image=root.view_3, text="View",text_color ="#808080",fg_color="#0A0A0A",text_font=("Helvetica 20 bold",10))
    root.stick.grid(row=4, column=1, pady=10, padx=10)

    root.cloud=ImageTk.PhotoImage(Image.open("cloud.png").resize((30, 30),Image.ANTIALIAS))
    root.view = customtkinter.CTkButton(master=root.frame_left, text="CLOUD",image=root.cloud,text_color ="#808080",fg_color="#0A0A0A",text_font=("Helvetica 20 bold",10), command=cloud)
    root.view.grid(row=5, column=1, pady=10, padx=10)
    
    root.Label = customtkinter.CTkLabel(root.frame_left, text="AI segmentation",bg="#0A0A0A",fg ="#ffffff",text_font=("Helvetica 20 bold",15))
    root.Label.grid(row=6, column=1, pady=10, padx=10)

    root.filter = customtkinter.CTkOptionMenu(master = root.frame_left, values=["leaukemia","malaria"], variable=root.var, text_color ="#808080",fg_color="#0A0A0A",text_font=("Helvetica 20 bold",10), command=filter_change)
    root.filter.grid(row=7, column=1, pady=10, padx=1)


    '''root.ai=ImageTk.PhotoImage(Image.open("ai.png").resize((60, 60),Image.ANTIALIAS))
    root.view = customtkinter.CTkButton(master=root.frame_left, text="AI segmentation",image=root.ai,text_color ="#808080",fg_color="#0A0A0A",text_font=("Helvetica 20 bold",10))
    root.view.grid(row=6, column=1, pady=10, padx=1)'''

    #root.frame_left.grid_rowconfigure(5, weight=1)

    root.Y = customtkinter.CTkButton(root.frame_left, width=30, text="Y+VE" ,text_color ="#808080",fg_color="#0A0A0A",text_font=("Helvetica 20 bold",10), command=up)
    root.Y.grid(row=8, column=1, padx=10, pady=10)

    root.y = customtkinter.CTkButton(root.frame_left, width=30, text="Y-VE",text_color ="#808080",fg_color="#0A0A0A",text_font=("Helvetica 20 bold",10), command=down)
    root.y.grid(row=9, column=1, padx=10, pady=10)

    root.X = customtkinter.CTkButton(root.frame_left, width=30, text="X+VE",text_color ="#808080",fg_color="#0A0A0A",text_font=("Helvetica 20 bold",10), command=right)
    root.X.grid(row=10, column=1, padx=10, pady=10)

    root.x = customtkinter.CTkButton(root.frame_left, width=30, text="X-VE",text_color ="#808080",fg_color="#0A0A0A",text_font=("Helvetica 20 bold",10), command=left)
    root.x.grid(row=11, column=1, padx=10, pady=10)

    root.H = customtkinter.CTkButton(root.frame_left, width=30,text="Home XY",text_color ="#808080",fg_color="#0A0A0A",text_font=("Helvetica 20 bold",10), command=home)
    root.H.grid(row=12, column=1, padx=10, pady=10)

    #root.frame_left.grid_rowconfigure(11, weight=1)

    #right
    root.bimage_3=ImageTk.PhotoImage(Image.open("login.png").resize((30, 30),Image.ANTIALIAS))
    root.button_3 = customtkinter.CTkButton(master=root.frame_right,text="",image=root.bimage_3,width=3,bg="#0A0A0A",fg_color="#0A0A0A",text_color ="#808080")
    root.button_3.grid(row=0, column=0, pady=10, padx=10,sticky="n")

    root.switch_1 = customtkinter.CTkSwitch(master=root.frame_right, text="A/M",text_color ="#808080",text_font=("Helvetica 20 bold",10),command=enable)
    root.switch_1.grid(row=1, column=0, columnspan=1, pady=10, padx=10)

    root.bimage_1=ImageTk.PhotoImage(Image.open("focus.png").resize((30, 30),Image.ANTIALIAS))
    root.button_1 = customtkinter.CTkButton(master=root.frame_right,text="", state=tk.DISABLED,image=root.bimage_1,width=3,bg="#0A0A0A",fg_color="#0A0A0A",text_color ="#808080", command=thread)
    root.button_1.grid(row=2, column=0, pady=10, padx=10)

    root.bimage_2=ImageTk.PhotoImage(Image.open("camera.png").resize((30, 30),Image.ANTIALIAS))
    root.button_2 = customtkinter.CTkButton(master=root.frame_right,text="",image=root.bimage_2,width=3,bg="#0A0A0A",fg_color="#0A0A0A",text_color ="#808080",command=Capture)
    root.button_2.grid(row=3, column=0, pady=10, padx=10)

    root.bimage_3=ImageTk.PhotoImage(Image.open("compare.png").resize((30, 30),Image.ANTIALIAS))
    root.button_3 = customtkinter.CTkButton(master=root.frame_right,text="",image=root.bimage_3,width=3,bg="#0A0A0A",fg_color="#0A0A0A",text_color ="#808080",command=preview)
    root.button_3.grid(row=4, column=0, pady=10, padx=10)

    root.rimage=ImageTk.PhotoImage(Image.open("report.png").resize((30, 30),Image.ANTIALIAS))
    root.report = customtkinter.CTkButton(master=root.frame_right,text="",image=root.rimage,width=3,bg="#0A0A0A",fg_color="#0A0A0A",text_color ="#808080")
    root.report.grid(row=5, column=0, pady=10, padx=10)

    root.frame_right.grid_rowconfigure(6, weight=1) 

    root.plus=ImageTk.PhotoImage(Image.open("plus.png").resize((30, 30),Image.ANTIALIAS))
    root.Z = customtkinter.CTkButton(root.frame_right, width=40, text="",image=root.plus,text_color ="#808080",fg_color="#0A0A0A", command=lambda: forward(1))
    root.Z.grid(row=7, column=0, padx=10, pady=10)

    root.home=ImageTk.PhotoImage(Image.open("home.png").resize((30, 30),Image.ANTIALIAS))
    root.h = customtkinter.CTkButton(root.frame_right, width=40, text="",image=root.home,text_color ="#808080",fg_color="#0A0A0A")
    root.h.grid(row=8, column=0, padx=10, pady=10)

    root.minus=ImageTk.PhotoImage(Image.open("minus.png").resize((30, 30),Image.ANTIALIAS))
    root.z = customtkinter.CTkButton(root.frame_right, width=40,text="",image=root.minus,text_color ="#808080",fg_color="#0A0A0A", command=lambda: backward(1))
    root.z.grid(row=9, column=0, padx=10, pady=10)

    root.frame_right.grid_rowconfigure(10, weight=1)

    root.helpimage=ImageTk.PhotoImage(Image.open("help.png").resize((30, 30),Image.ANTIALIAS))
    root.help = customtkinter.CTkButton(master=root.frame_right,text="",image=root.helpimage,width=3,bg="#0A0A0A",fg_color="#0A0A0A",text_color ="#808080")
    root.help.grid(row=11, column=0, pady=10, padx=10)
    
    root.Quit =ImageTk.PhotoImage(Image.open("image.png").resize((30, 30),Image.ANTIALIAS))
    root.Quit = customtkinter.CTkButton(master=root.frame_right, width=3, image=root.Quit, text="", command=root.destroy, bg="#0A0A0A",fg_color="#0A0A0A",text_color ="#808080")
    root.Quit.grid(row=12, column=0, padx=10, pady=10)

    ShowFeed()

def ShowFeed():
    # Capturing frame by frame
    frame = root.cap.read()
    #frame = imutils.resize(frame,width = 720*2, height = 960*2)
    #frame = imutils.resize(frame,width1-200,height1-200)
    #print('Resolution: ' + str(frame.shape[0]) + ' x ' + str(frame.shape[1]))
    
    #cv2.putText(frame, datetime.now().strftime('%d/%m/%Y %H:%M:%S'), (20,30), cv2.FONT_HERSHEY_DUPLEX, 0.6, (255,255,255))
    #cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    #b,g,r = cv2.split(cv2image)
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = canny(gray)
    cv2.putText(frame, datetime.now().strftime('%d/%m/%Y %H:%M:%S')+str("  ")+str("blurness")+str("  ")+str(int(blur)), (20,30), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0,255,255))
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    b,g,r = cv2.split(cv2image)
    
    global x
    if x == "Red":
        fil = r
    elif x == "Green":
        fil = g
    elif x == "Blue":
        fil = b
    elif x == "Normal":
        fil = cv2image
    elif x == "Segmentation":
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
        cnts, heir = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cv2image2 = cv2.drawContours(frame,cnts,-1,(0,255,0),3)
        fil = cv2image2
    elif x == "leaukemia":
        hsvFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) 

        red_lower = np.array([136, 87, 111], np.uint8) 
        red_upper = np.array([199, 125, 212], np.uint8) 
        red_mask = cv2.inRange(hsvFrame, red_lower, red_upper) 

        kernal = np.ones((5, 5), "uint8") 

        contours, hierarchy = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) 
        cv2image2=cv2.drawContours(frame,contours,-1,(199, 125, 212),3)
        fil = cv2image2
    elif x == "malaria":
        hsvFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) 

        red_lower = np.array([136, 87, 111], np.uint8) 
        red_upper = np.array([180, 255, 255], np.uint8) 
        red_mask = cv2.inRange(hsvFrame, red_lower, red_upper) 

        kernal = np.ones((5, 5), "uint8") 

        contours, hierarchy = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) 
        cv2image2=cv2.drawContours(frame,contours,-1,(180, 255, 255),3)
        fil = cv2image2
            
    videoImg = Image.fromarray(fil)
    imgtk = ImageTk.PhotoImage(image = videoImg)
    root.cameraLabel.configure(image=imgtk)
    root.cameraLabel.imgtk = imgtk
    root.cameraLabel.after(10, ShowFeed)

def enable():
    if root.switch_1.get():
        root.button_1.configure(state=tk.NORMAL)
        root.Z.configure(state=tk.DISABLED)
        root.z.configure(state=tk.DISABLED)
        root.h.configure(state=tk.DISABLED)

    else:
        root.button_1.configure(state=tk.DISABLED)
        root.Z.configure(state=tk.NORMAL)
        root.z.configure(state=tk.NORMAL)
        root.h.configure(state=tk.NORMAL)

def Capture():
    destDirectory = filedialog.askdirectory(initialdir="YOUR DIRECTORY PATH")
    destPath.set(destDirectory)
    image_name = datetime.now().strftime('%d-%m-%Y %H-%M-%S')
    if destPath.get() != '':
        image_path = destPath.get()
    else:
        messagebox.showerror("ERROR", "NO DIRECTORY SELECTED TO STORE IMAGE!!")

    imgName = image_path + '/' + image_name + ".jpg"
    frame = root.cap.read()
    cv2.putText(frame, datetime.now().strftime('%d/%m/%Y %H:%M:%S'), (20,30), cv2.FONT_HERSHEY_DUPLEX, 0.5, (255,255,255))
    success = cv2.imwrite(imgName, frame)

    if success :
        messagebox.showinfo("SUCCESS", "IMAGE CAPTURED AND SAVED IN " + imgName)

def filter_change(filter):
    global x
    x = filter

def preview():

    def imageBrowse():
        openDirectory = filedialog.askopenfilename(initialdir="YOUR DIRECTORY PATH")
        imagePath.set(openDirectory)
        imageView = Image.open(openDirectory)
        imageResize = imageView.resize((740, 500), Image.ANTIALIAS)
        imageDisplay = ImageTk.PhotoImage(imageResize)
        pre.imageLabel.configure(image=imageDisplay)
        pre.imageLabel.photo = imageDisplay

    pre = customtkinter.CTkToplevel()

    pre.previewlabel = customtkinter.CTkLabel(pre, bg="#0A0A0A",fg ="#ffffff", text="select file to be uploaded")
    pre.previewlabel.grid(row=1, column=1, padx=10, pady=10, columnspan=2)
 
    pre.imageLabel = customtkinter.CTkLabel(pre, borderwidth=3, relief="groove", text="Select Image")
    pre.imageLabel.grid(row=2, column=1, padx=10, pady=10, columnspan=2)

    pre.openImageButton = customtkinter.CTkButton(pre, width=10, text="BROWSE",text_color ="#808080",fg_color="#0A0A0A", command=imageBrowse)
    pre.openImageButton.grid(row=3, column=1, padx=10, pady=10,columnspan=2)

    pre.grid_columnconfigure(4, weight=1)

    pre.Quit = customtkinter.CTkButton(pre, width=10, text="QUIT", command=pre.destroy,text_color ="#808080",fg_color="#0A0A0A")
    pre.Quit.grid(row=0, column=6, padx=10, pady=10, columnspan=2) 

    pre.title("upload file")
    pre.geometry(f'{width1}x{height1}')
    pre.resizable(True, True)

    pre.mainloop()
    
def forward(steps):
    mymotortest.motor_go(True,"Full", steps, 0.0076, False, 0.05)

def backward(steps):
    mymotortest.motor_go(False,"Full", steps, 0.0076, False, 0.05)
    
def thread():
    t1 = threading.Thread(target=motor)
    t2 = threading.Thread(target=blur)
    
    if root.switch_1.get():
        try:
            global re
            file = open("steps1.txt","r")
            re = int(file.read())
            file.close()
        except:
            file = open("steps1.txt","w")
            file.write("0")
            file.close()
            re = 0
        if (re>1 or re ==0):
            mymotortest.motor_go(False, "Full", re, 0.0009, False, 0.05)
            print("return")
            
        t1.start()
        t2.start()
        t1.join()
        t2.join()

def canny(img):
    canny_var = cv2.Canny(img,100,200).var()
    return canny_var

def motor():
    global start
    start1 = time.time()
    mymotortest.motor_go(True, "Full", 1000, 0.0078, False, 0.05)
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
            crop = frame[70:460, 110:490]
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            canny_var = canny(gray)
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
    
def cloud():
    
    openDirectory = filedialog.askopenfilename(initialdir="your directory path")
    imagePath.set(openDirectory)
    gauth = GoogleAuth()
    drive = GoogleDrive(gauth)
    upload_file_list = [openDirectory]
    for upload_file in upload_file_list:
        gfile = drive.CreateFile({'parents': [{'id': 'inM5vBDADIykaBaOi5X02WhQeiwSQxovk'}]})
        gfile.SetContentFile(upload_file)
        gfile.Upload()
        
    
root = customtkinter.CTk() 

root.var = customtkinter.StringVar(value="Normal")
destPath = customtkinter.StringVar()
imagePath = customtkinter.StringVar()

width1 = root.winfo_screenwidth()
height1 = root.winfo_screenheight()
print(width1,height1)

root.title("IMEAD")
root.geometry(f'{width1}x{height1}')

root.resizable(True, True)
root.attributes('-fullscreen', True)
#root.cap = VideoStream(src=0, usePiCamera=True, resolution=(960,720)).start()
root.cap = VideoStream(src=0).start()
#root.cap.stream.set(3, 1920)
#root.cap.stream.set(4, 1080)
#root.cap = cv2.VideoCapture(1)
# Setting width and height
#width, height = 1920,1080
#root.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
#root.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
#root.cap.set(cv2.CAP_PROP_FPS, 60)
window()
root.mainloop()
