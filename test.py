import tkinter
import tkinter.messagebox
import customtkinter
import cv2
from datetime import datetime
from PIL import Image, ImageTk
from tkinter import messagebox, filedialog

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

def ShowFeed():
    # Capturing frame by frame
    ret, frame = root.cap.read()

    if ret:
        # Flipping the frame vertically
        frame = cv2.flip(frame, 1)

        # Displaying date and time on the feed
        cv2.putText(frame, datetime.now().strftime('%d/%m/%Y %H:%M:%S'), (20,30), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0,255,255))

        # Changing the frame color from BGR to RGB
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)

        # Creating an image memory from the above frame exporting array interface
        videoImg = Image.fromarray(cv2image)

        # Creating object of PhotoImage() class to display the frame
        imgtk = ImageTk.PhotoImage(image = videoImg)

        # Configuring the label to display the frame
        root.cameraLabel.configure(image=imgtk)

        # Keeping a reference
        root.cameraLabel.imgtk = imgtk

        # Calling the function after 10 milliseconds
        root.cameraLabel.after(10, ShowFeed)
    else:
        # Configuring the label to display the frame
        root.cameraLabel.configure(image='')

def destBrowse():
    # Presenting user with a pop-up for directory selection. initialdir argument is optional
    # Retrieving the user-input destination directory and storing it in destinationDirectory
    # Setting the initialdir argument is optional. SET IT TO YOUR DIRECTORY PATH
    destDirectory = filedialog.askdirectory(initialdir="YOUR DIRECTORY PATH")

    # Displaying the directory in the directory textbox
    destPath.set(destDirectory)

def imageBrowse():
    # Presenting user with a pop-up for directory selection. initialdir argument is optional
    # Retrieving the user-input destination directory and storing it in destinationDirectory
    # Setting the initialdir argument is optional. SET IT TO YOUR DIRECTORY PATH
    openDirectory = filedialog.askopenfilename(initialdir="YOUR DIRECTORY PATH")

    # Displaying the directory in the directory textbox
    imagePath.set(openDirectory)

    # Opening the saved image using the open() of Image class which takes the saved image as the argument
    imageView = Image.open(openDirectory)

    # Resizing the image using Image.resize()
    imageResize = imageView.resize((640, 480), Image.ANTIALIAS)

    # Creating object of PhotoImage() class to display the frame
    imageDisplay = ImageTk.PhotoImage(imageResize)

    # Configuring the label to display the frame
    root.imageLabel.config(image=imageDisplay)

    # Keeping a reference
    root.imageLabel.photo = imageDisplay

# Defining Capture() to capture and save the image and display the image in the imageLabel
def Capture():
    # Storing the date in the mentioned format in the image_name variable
    image_name = datetime.now().strftime('%d-%m-%Y %H-%M-%S')

    # If the user has selected the destination directory, then get the directory and save it in image_path
    if destPath.get() != '':
        image_path = destPath.get()
    # If the user has not selected any destination directory, then set the image_path to default directory
    else:
        messagebox.showerror("ERROR", "NO DIRECTORY SELECTED TO STORE IMAGE!!")

    # Concatenating the image_path with image_name and with .jpg extension and saving it in imgName variable
    imgName = image_path + '/' + image_name + ".jpg"

    # Capturing the frame
    ret, frame = root.cap.read()

    # Displaying date and time on the frame
    cv2.putText(frame, datetime.now().strftime('%d/%m/%Y %H:%M:%S'), (430,460), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0,255,255))

    # Writing the image with the captured frame. Function returns a Boolean Value which is stored in success variable
    success = cv2.imwrite(imgName, frame)

    # Opening the saved image using the open() of Image class which takes the saved image as the argument
    saved_image = Image.open(imgName)

    # Creating object of PhotoImage() class to display the frame
    saved_image = ImageTk.PhotoImage(saved_image)

    # Configuring the label to display the frame
    root.imageLabel.config(image=saved_image)

    # Keeping a reference
    root.imageLabel.photo = saved_image

    # Displaying messagebox
    if success :
        messagebox.showinfo("SUCCESS", "IMAGE CAPTURED AND SAVED IN " + imgName)


def StopCAM():
    # Stopping the camera using release() method of cv2.VideoCapture()
    root.cap.release()

    # Configuring the CAMBTN to display accordingly
    root.CAMBTN.config(text="START CAMERA", command=StartCAM)

    # Displaying text message in the camera label
    root.cameraLabel.config(text="OFF CAM", font=('Comic Sans MS',70))

def StartCAM():
    # Creating object of class VideoCapture with webcam index
    root.cap = cv2.VideoCapture(0)

    # Setting width and height
    width_1, height_1 = 640, 480
    root.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width_1)
    root.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height_1)

    # Configuring the CAMBTN to display accordingly
    root.CAMBTN.config(text="STOP CAMERA", command=StopCAM)

    # Removing text message from the camera label
    root.cameraLabel.config(text="")

    # Calling the ShowFeed() Function
    ShowFeed()



def change_appearance_mode(new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)


root = customtkinter.CTk() 

width = root.winfo_screenwidth()
height = root.winfo_screenheight()

destPath = tkinter.StringVar()
imagePath = tkinter.StringVar()

root.title("Pycam")
root.geometry(f'{width}x{height}')
root.resizable(True, True)
#root.configure(background = "sky blue")

root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(0, weight=1)

root.frame_left = customtkinter.CTkFrame(master=root,width=180,corner_radius=0)
root.frame_left.grid(row=0, column=0, sticky="nswe")

root.frame_right = customtkinter.CTkFrame(master=root)
root.frame_right.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)
#root.frame_left.grid_rowconfigure(0, minsize=10)   # empty row with minsize as spacing
root.frame_left.grid_rowconfigure(8, weight=1)  # empty row as spacing
#root.frame_left.grid_rowconfigure(8, minsize=20)    # empty row with minsize as spacing
#root.frame_left.grid_rowconfigure(11, minsize=10)  # empty row with minsize as spaciroot

#left frame
root.label_1 = customtkinter.CTkLabel(master=root.frame_left, text="IMEAD")  # font name and size in px
root.label_1.grid(row=1, column=0, pady=10, padx=10)

root.button_1 = customtkinter.CTkButton(master=root.frame_left, text="Start Camera")
root.button_1.grid(row=2, column=0, pady=10, padx=20)

root.button_2 = customtkinter.CTkButton(master=root.frame_left, text="Stop Camera")
root.button_2.grid(row=3, column=0, pady=10, padx=20)

root.button_3 = customtkinter.CTkButton(master=root.frame_left, text="Autofocus")
root.button_3.grid(row=7, column=0, pady=10, padx=20)

root.label_mode = customtkinter.CTkLabel(master=root.frame_left, text="Appearance Mode:")
root.label_mode.grid(row=9, column=0, pady=0, padx=20, sticky="w")

root.switch_1 = customtkinter.CTkSwitch(master=root.frame_left, text="Manual")
root.switch_1.grid(row=5, column=0, columnspan=1, pady=10, padx=20, sticky="w")

root.switch_2 = customtkinter.CTkSwitch(master=root.frame_left, text="Automatic")
root.switch_2.grid(row=6, column=0, columnspan=1, pady=10, padx=20, sticky="w")

root.captureBTN = customtkinter.CTkButton(master=root.frame_left, text="CAPTURE", command=Capture)
root.captureBTN.grid(row=4, column=0, columnspan=1, pady=10, padx=20, sticky="w")

root.optionmenu_1 = customtkinter.CTkOptionMenu(master=root.frame_left, values=["Light", "Dark", "System"], command=change_appearance_mode)
root.optionmenu_1.grid(row=10, column=0, pady=10, padx=20, sticky="w")


#right frame
root.feedlabel = customtkinter.CTkLabel(root.frame_right, bg="steelblue", fg="white", text="WEBCAM FEED")
root.feedlabel.grid(row=1, column=1, padx=10, pady=10, columnspan=2)
    #for camera feed
root.cameraLabel = customtkinter.CTkLabel(root.frame_right, bg="steelblue", borderwidth=3, relief="groove")
root.cameraLabel.grid(row=2, column=1, padx=10, pady=10, columnspan=2)

root.saveLocationEntry = customtkinter.CTkEntry(root.frame_right, width=55, textvariable=destPath)
root.saveLocationEntry.grid(row=3, column=1, padx=10, pady=10)

root.browseButton = customtkinter.CTkButton(root.frame_right, width=10, text="BROWSE", command=destBrowse)
root.browseButton.grid(row=3, column=2, padx=10, pady=10)

root.previewlabel = customtkinter.CTkLabel(root.frame_right, bg="steelblue", fg="white", text="IMAGE PREVIEW")
root.previewlabel.grid(row=1, column=4, padx=10, pady=10, columnspan=2)

root.imageLabel = customtkinter.CTkLabel(root.frame_right, bg="steelblue", borderwidth=3, relief="groove")
root.imageLabel.grid(row=2, column=4, padx=10, pady=10, columnspan=2)

root.openImageEntry = customtkinter.CTkEntry(root.frame_right, width=55, textvariable=imagePath)
root.openImageEntry.grid(row=3, column=4, padx=10, pady=10)

root.openImageButton = customtkinter.CTkButton(root.frame_right, width=10, text="BROWSE")
root.openImageButton.grid(row=3, column=5, padx=10, pady=10)



root.mainloop()