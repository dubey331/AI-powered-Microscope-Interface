import tkinter
import customtkinter
#import RPi.GPIO as GPIO
#from RpiMotorLib import RpiMotorLib

customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue") 

app = customtkinter.CTk()  # create CTk window like you do with the Tk window
app.geometry("400x240")

GPIO_pins = (16, 12, 6) 
direction = 21      
step = 20

#mymotortest = RpiMotorLib.A4988Nema(direction, step, GPIO_pins, "A4988")

def motor(dir, steps):
    print(dir,steps)
    #mymotortest.motor_go(dir,"Full", steps, 0.0076, False, 0.05)

def forward(steps):
    print("forward",steps)
    #mymotortest.motor_go(True,"Full", steps, 0.0076, False, 0.05)

def backward(steps):
    print("backward",steps)
    #mymotortest.motor_go(False,"Full", steps, 0.0076, False, 0.05)

button = customtkinter.CTkButton(master=app, text="motor", command=lambda: motor(True, 10))
button.pack(padx = 10, pady = 10)

button = customtkinter.CTkButton(master=app, text="forward", command=lambda: forward(10))
button.pack(padx = 10, pady = 10)

button = customtkinter.CTkButton(master=app, text="backward", command=lambda: backward(10))
button.pack(padx = 10, pady = 10)

app.mainloop()