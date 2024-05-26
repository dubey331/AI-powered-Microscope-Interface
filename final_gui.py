from re import X
import tkinter as tk
import customtkinter
import cv2
from datetime import datetime
from PIL import Image, ImageTk
from tkinter import messagebox, filedialog

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"

global x
x="Normal"

def window():
    root.grid_columnconfigure(1, weight=1)
    root.grid_rowconfigure(0, weight=1)

    root.frame_left = customtkinter.CTkFrame(master=root, corner_radius=1, width= 400)
    root.frame_left.pack(side="left", fill="both", padx=10, pady=10)

    root.frame_right = customtkinter.CTkFrame(master=root, corner_radius=1, width= 400)
    root.frame_right.pack(side="right", fill="both", padx=5, pady=10)

    root.frame_center = customtkinter.CTkFrame(master=root, corner_radius=1)
    root.frame_center.pack(side="top", fill="both", padx=5, pady=10)

    root.frame_lower = customtkinter.CTkFrame(master=root, corner_radius=1)
    root.frame_lower.pack(side="bottom", fill="both", padx=5, pady=10, expand=True)

    root.frame_right.grid_rowconfigure(10, weight=1) 
    root.frame_lower.grid_columnconfigure(6, weight=1) 
    root.frame_left.grid_rowconfigure(4, weight=1)

    #left frame
    root.label_1 = customtkinter.CTkLabel(master=root.frame_left, text="IMEAD", text_font=("Helvetica 20 bold",40))  # font name and size in px
    root.label_1.grid(row=1, column=0, pady=10, padx=10)
    
    root.help = customtkinter.CTkButton(master=root.frame_left, text="HELP")
    root.help.grid(row=2, column=0, pady=10, padx=10)

    root.about = customtkinter.CTkButton(master=root.frame_left, text="ABOUT US")
    root.about.grid(row=3, column=0, pady=10, padx=10)

    root.label_mode = customtkinter.CTkLabel(master=root.frame_left, text="Appearance Mode:")
    root.label_mode.grid(row=6, column=0, pady=0, padx=10)

    root.optionmenu_1 = customtkinter.CTkOptionMenu(master=root.frame_left, values=["Light", "Dark", "System"], command=change_appearance_mode)
    root.optionmenu_1.grid(row=7, column=0, pady=10, padx=10)

    #right frame
    root.captureBTN = customtkinter.CTkButton(master=root.frame_right, text="CAPTURE", command=Capture)
    root.captureBTN.grid(row=1, column=0, columnspan=1, pady=10, padx=10)

    root.switch_1 = customtkinter.CTkSwitch(master=root.frame_right, text="Automatic", command=enable)
    root.switch_1.grid(row=2, column=0, columnspan=1, pady=10, padx=10)

    root.button_3 = customtkinter.CTkButton(master=root.frame_right, text="Autofocus", state=tk.DISABLED)
    root.button_3.grid(row=3, column=0, pady=10, padx=10)

    root.button_4 = customtkinter.CTkButton(master=root.frame_right, text="Preview", command=preview)
    root.button_4.grid(row=4, column=0, pady=10, padx=10)

    root.filter_label = customtkinter.CTkLabel(master=root.frame_right, text="Filters", text_font=("Helvetica 20 bold",20))
    root.filter_label.grid(row=5, column=0, pady=10, padx=10)

    root.filter = customtkinter.CTkOptionMenu(master = root.frame_right, values=["Normal","Red","Green","Blue"], command=filter_change, variable=root.var)
    root.filter.grid(row=6, column=0, pady=10, padx=10)

    root.cloud = customtkinter.CTkButton(master=root.frame_right, text="Cloud")
    root.cloud.grid(row=7, column=0, pady=10, padx=10)

    root.stick = customtkinter.CTkButton(master=root.frame_right, text="Image Stitching")
    root.stick.grid(row=8, column=0, pady=10, padx=10)

    root.CAMBTN = customtkinter.CTkButton(master= root.frame_right, text="STOP CAMERA", command=StopCAM)
    root.CAMBTN.grid(row=9, column=0, pady=10, padx=2)

    root.Q = customtkinter.CTkButton(root.frame_right, text="Quit", command=root.quit)
    root.Q.grid(row=11, column=0, padx=10, pady=10)
    
    #center frame
    root.feedlabel = customtkinter.CTkLabel(root.frame_center, text="Camera Feed", text_font=("Helvetica 20 bold",20))
    root.feedlabel.grid(row=1, column=1, padx=10, pady=5, columnspan=2)
    
    root.cameraLabel = customtkinter.CTkLabel(root.frame_center, borderwidth=2, relief="groove")
    root.cameraLabel.grid(row=2, column=1, padx=10, pady=5, columnspan=2)

    root.saveLocationEntry = customtkinter.CTkEntry(root.frame_center, textvariable=destPath, width=550)
    root.saveLocationEntry.grid(row=3, column=1, padx=10, pady=10)

    root.browseButton = customtkinter.CTkButton(root.frame_center, width=10, text="BROWSE", command=destBrowse)
    root.browseButton.grid(row=3, column=2, padx=10, pady=10)
    
    #lower frame
    root.joystick = customtkinter.CTkLabel(root.frame_lower, width=10, text="Joystick", text_font=("Helvetica 20 bold",20))
    root.joystick.grid(row=1, column=1, padx=10, pady=10, columnspan=4)

    root.Y = customtkinter.CTkButton(root.frame_lower, width=40, text="Y+VE")
    root.Y.grid(row=2, column=2, padx=10, pady=10)

    root.y = customtkinter.CTkButton(root.frame_lower, width=40, text="Y-VE")
    root.y.grid(row=4, column=2, padx=10, pady=10)

    root.X = customtkinter.CTkButton(root.frame_lower, width=40, text="X+VE")
    root.X.grid(row=3, column=3, padx=10, pady=10)

    root.x = customtkinter.CTkButton(root.frame_lower, width=40, text="X-VE")
    root.x.grid(row=3, column=1, padx=10, pady=10)

    root.Z = customtkinter.CTkButton(root.frame_lower, width=40, text="Z+VE")
    root.Z.grid(row=2, column=4, padx=10, pady=10)

    root.z = customtkinter.CTkButton(root.frame_lower, width=40, text="Z-VE")
    root.z.grid(row=4, column=4, padx=10, pady=10)

    root.H = customtkinter.CTkButton(root.frame_lower, width=40, text="Home XY")
    root.H.grid(row=3, column=2, padx=10, pady=10)

    root.h = customtkinter.CTkButton(root.frame_lower, width=40, text="Home Z")
    root.h.grid(row=3, column=4, padx=10, pady=10)

    ShowFeed()

def preview():

    def imageBrowse():
        openDirectory = filedialog.askopenfilename(initialdir="YOUR DIRECTORY PATH")
        imagePath.set(openDirectory)
        imageView = Image.open(openDirectory)
        imageResize = imageView.resize((1280, 720), Image.ANTIALIAS)
        imageDisplay = ImageTk.PhotoImage(imageResize)
        pre.imageLabel.configure(image=imageDisplay)
        pre.imageLabel.photo = imageDisplay

    pre = customtkinter.CTkToplevel()

    pre.previewlabel = customtkinter.CTkLabel(pre, bg="steelblue", fg="white", text="IMAGE PREVIEW")
    pre.previewlabel.grid(row=1, column=1, padx=10, pady=10, columnspan=2)

    pre.imageLabel = customtkinter.CTkLabel(pre, borderwidth=3, relief="groove", text="Select Image")
    pre.imageLabel.grid(row=2, column=1, padx=10, pady=10, columnspan=2)

    pre.openImageEntry = customtkinter.CTkEntry(pre, width=450, textvariable=imagePath)
    pre.openImageEntry.grid(row=3, column=1, padx=10, pady=10)

    pre.openImageButton = customtkinter.CTkButton(pre, width=10, text="BROWSE", command=imageBrowse)
    pre.openImageButton.grid(row=3, column=2, padx=10, pady=10)

    #pre.grid_rowconfigure(5, weight=1)

    pre.Quit = customtkinter.CTkButton(pre, width=10, text="QUIT", command=pre.destroy)
    pre.Quit.grid(row=6, column=1, padx=10, pady=10, columnspan=2) 

    pre.title("Preview")
    pre.geometry(f'{width1}x{height1}')
    pre.resizable(True, True)

    pre.mainloop()
    
def filter_change(filter):
    global x
    x = filter

def ShowFeed():
    # Capturing frame by frame
    ret, frame = root.cap.read()
    if ret:
        frame = cv2.flip(frame, 1)
        print('Resolution: ' + str(frame.shape[0]) + ' x ' + str(frame.shape[1]))
        cv2.putText(frame, datetime.now().strftime('%d/%m/%Y %H:%M:%S'), (20,30), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0,255,255))
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
        videoImg = Image.fromarray(fil)
        imgtk = ImageTk.PhotoImage(image = videoImg)
        root.cameraLabel.configure(image=imgtk)
        root.cameraLabel.imgtk = imgtk
        root.cameraLabel.after(10, ShowFeed)
    else:
        root.cameraLabel.configure(image='')

def StopCAM():
    root.cap.release()
    root.CAMBTN.configure(text="START CAMERA", command=StartCAM)
    root.cameraLabel.configure(text="OFF CAM")

def StartCAM():
    root.cap = cv2.VideoCapture(0)

    width_1, height_1 = 640, 480
    root.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc('m','j','p','g'))
    root.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc('M','J','P','G'))
    root.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width_1)
    root.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height_1)

    root.CAMBTN.configure(text="STOP CAMERA", command=StopCAM)
    root.cameraLabel.configure(text="")
    ShowFeed()

def destBrowse():
    destDirectory = filedialog.askdirectory(initialdir="YOUR DIRECTORY PATH")
    destPath.set(destDirectory)

def Capture():
    image_name = datetime.now().strftime('%d-%m-%Y %H-%M-%S')
    if destPath.get() != '':
        image_path = destPath.get()
    else:
        messagebox.showerror("ERROR", "NO DIRECTORY SELECTED TO STORE IMAGE!!")

    imgName = image_path + '/' + image_name + ".jpg"
    ret, frame = root.cap.read()
    cv2.putText(frame, datetime.now().strftime('%d/%m/%Y %H:%M:%S'), (430,460), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0,255,255))
    success = cv2.imwrite(imgName, frame)

    if success :
        messagebox.showinfo("SUCCESS", "IMAGE CAPTURED AND SAVED IN " + imgName)

def change_appearance_mode(new_appearance_mode):
    customtkinter.set_appearance_mode(new_appearance_mode)

def enable():
    if root.switch_1.get():
        root.button_3.configure(state=tk.NORMAL)
        root.Z.configure(state=tk.DISABLED)
        root.z.configure(state=tk.DISABLED)
        root.h.configure(state=tk.DISABLED)

    else:
        root.button_3.configure(state=tk.DISABLED)
        root.Z.configure(state=tk.NORMAL)
        root.z.configure(state=tk.NORMAL)
        root.h.configure(state=tk.NORMAL)


root = customtkinter.CTk() 

width1 = root.winfo_screenwidth()
height1 = root.winfo_screenheight()

root.cap = cv2.VideoCapture(0)

# Setting width and height
width, height = 640, 480
root.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc('m','j','p','g'))
root.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc('M','J','P','G'))
root.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
root.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

root.var = customtkinter.StringVar(value="Normal")

destPath = tk.StringVar()
imagePath = tk.StringVar()

root.title("Microscope")
root.geometry(f'{width1}x{height1}')
root.resizable(True, True)

window()
root.mainloop()