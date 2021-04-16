""" receive_jpg_images.py -- receive & display jpg stream.

A simple test program that uses imagezmq to receive an image jpg stream from a
Raspberry Pi and display it as a video steam.

1. Run this program in its own window on windows:
python receive_jpg_images.py

This "receive and display images" program must be running before starting the
RasPi sending program.

2. Run the jpg sending program on the RPi:
python send_jpg_images.py

A cv2.imshow() window will appear on the PC showing the tramsmitted images as
a video stream. You can repeat Step 2 and start the test_3_rpi_send_jpg.py on
multiple RPis and each one will cause a new cv2.imshow() window to open.

To end the programs, press Ctrl-C in the terminal window of the RasPi first.
Then press "q" in the display window of the receiving proram. You may have 
to press Ctrl-C in the terminal window as well.
"""

import numpy as np
import cv2
import imagezmq
import time
import socket

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

image_hub = imagezmq.ImageHub()

host_name = socket.gethostname()  # send RPi hostname with each image
IP_Addr = get_ip()    
print("Your Computer Name is:" + host_name)    
print("Host 2 receiving images at IP Address: " + IP_Addr + ':5555') 

frame_number=0; # this variable is used to count the frames
prev_frame_number=frame_number
previous_seconds = time.time()
fps=0
while True:  # show streamed images until Ctrl-C
    frame_number=frame_number+1 # count each frame that is processed

    rpi_name, jpg_buffer = image_hub.recv_jpg()
    image = cv2.imdecode(np.frombuffer(jpg_buffer, dtype='uint8'), -1)


    seconds = time.time()
    elapsed_seconds = seconds - previous_seconds
    if elapsed_seconds > 5:
        fps= (frame_number-prev_frame_number) / elapsed_seconds
        prev_frame_number=frame_number
        previous_seconds = seconds

    # print frame number on image
    cv2.putText(image, 'FPS = %.1f' %(fps), (10, 30), cv2.FONT_HERSHEY_SIMPLEX,1.0, (0, 255, 0), 2)

    # see opencv docs for info on -1 parameter
    cv2.imshow(rpi_name, image)  # 1 window for each RPi

    # if the 'q' key is pressed, stop the loop
    key = cv2.waitKey(1)
    if key == 27 or key == ord("q"):
        break
    image_hub.send_reply(b'OK')

# close any open windows
cv2.destroyAllWindows()


