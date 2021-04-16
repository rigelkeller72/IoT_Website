import sys
import socket
import time
import cv2
from imutils.video import VideoStream
import imagezmq


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

# Create an image sender in PUB/SUB (non-blocking) mode
sender = imagezmq.ImageSender(connect_to='tcp://*:5555', REQ_REP=False)
host_name = socket.gethostname()  # send RPi hostname with each image
IP_Addr = get_ip()    
print("Your Computer Name is:" + host_name)    
print("HOST 1 sending images from IP Address: " + IP_Addr + ':5555') 

#cam = VideoStream(usePiCamera=True).start()
cam = VideoStream(0).start() # open camera
time.sleep(2.0)  # allow camera sensor to warm up

jpeg_quality = 30  # 0 to 100, higher is better quality, 95 is cv2 default

image_window_name = host_name
i = 0
while True:  # press Ctrl-C to stop image sending program
    # Increment a counter and print it's current state to console
    i = i + 1
##    print('  Sending image %d' %( i)) # 

    # read image from webcam
    # Add an incrementing counter to the image
    image = cam.read()
    cv2.putText(image, str(i), (10,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 4)

    # encode image into JPEG format (compressed)
    ret_code, jpg_image = cv2.imencode(".jpg", image, [int(cv2.IMWRITE_JPEG_QUALITY), jpeg_quality])
    # Send an image to the queue
    sender.send_jpg(host_name, jpg_image) # send image

    time.sleep(0.25) # in seconds
