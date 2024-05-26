import cv2
import os
import serial
import sys
import scf4_tools
import time
import threading
import camera

CHC_MOVE    = 8
CHB_MOVE    = 7
CHA_MOVE    = 6
CHC_PI      = 5
CHB_PI      = 4
CHA_PI      = 3
CHC_POS     = 2
CHB_POS     = 1
CHA_POS     = 0

ser = serial.Serial()
ser.port = '/dev/cu.usbmodem1101'              # Controller com port
ser.baudrate = 115200           # BAUD rate when connected over CDC USB is not important
ser.timeout = 5                 # max timeout to wait for command response

print("Open COM port:", ser.port)
ser.open()
ser.flushInput()
ser.flushOutput()

c = camera.Cam()
print("Starting cam")
c.start()

# define ROI center of the frame
roi_size = 100
x0 = int(1920/2-roi_size)
x1 = int(1920/2+roi_size)
y0 = int(1080/2-roi_size)
y1 = int(1080/2+roi_size)
#c.focus_tracker(True, x0, x1, y0, y1)

print("Waiting for camera")
while c.fps == 0:
    time.sleep(0.1) # should be implemented with queue/signals but good enough for testing
print("Cam is operational")

c.set_cam_text("Prepare")

c.set_cam_text("Homing")
print("Home z axis")
l = 'G28 Z0'+'\n'
ser.write(l.encode())

'''scf4_tools.send_command(ser, "G28 Z0", echo=True)
status_str = scf4_tools.send_command(ser, "!1")
status = scf4_tools.parse_status(status_str)
print(status_str)'''

#TODO: sweep full focus range and measure focus table
#TODO: go to best focus position


while True:
    c.set_cam_text("Click mouse on the image to autofocus")
    time.sleep(0.1)

    if c.mouse_clicked:
        c.mouse_clicked = False
        focus_table = []
    
        #c.set_cam_text("Moving to MIN foxus point")
        #scf4_tools.send_command(ser, "G0 B29000")
        #scf4_tools.wait_homing(ser, 1, CHB_MOVE)

        #scf4_tools.send_command(ser, "M240 B5000")    # make motor move slower
        c.set_cam_text("Searching for best focus position (full range)")
        #scf4_tools.send_command(ser, "G0 B38000")
        l='G21G90G1Z5F200'+'\n'
        ser.write(l.encode())

        for i in range(10000):
            #status_str = scf4_tools.send_command(ser, "!1")
            #status = scf4_tools.parse_status(status_str)
            #print(status[1], c.focus_val)
            focus_table.append([i, c.focus_val])
            time.sleep(0.01)
            
        time.sleep(0.1)

        focus_peak_val = -1
        focus_peak_pos = -1

        for f in focus_table:
            if f[1] > focus_peak_val:
                focus_peak_pos= f[0]
                focus_peak_val = f[1]
        
        print()
        print("Best focus pos:", focus_peak_pos)
        print("Best focus val:", focus_peak_val)
        
        # experimental offset value. due to camera frame and motor mismatch
        #focus_peak_pos -= 100
        #scf4_tools.send_command(ser, "M240 B600")    # make motor move normal

        c.set_cam_text("Moving to best position")
        l='G21G90G1Z-'+str(focus_peak_pos)+'\n'
        #scf4_tools.send_command(ser, "G0 B"+str(focus_peak_pos))
        #scf4_tools.wait_homing(ser, 1, CHB_MOVE)


    if not c.running:
        break

print("Stopping camera")

c.stop()

