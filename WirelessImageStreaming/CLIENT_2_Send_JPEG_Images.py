import socket
import time
import cv2
from imutils.video import VideoStream
import imagezmq

Send_To_Address = 'tcp://10.25.62.125:5555'

# use the formats below to specifiy address of display computer
sender = imagezmq.ImageSender(connect_to=Send_To_Address)

print('CLIENT 2 sending images to:',Send_To_Address)

rpi_name = socket.gethostname()  # send RPi hostname with each image

#cam = VideoStream(usePiCamera=True).start()
cam = VideoStream(0).start() # open camera
time.sleep(2.0)  # allow camera sensor to warm up

jpeg_quality = 30  # 0 to 100, higher is better quality, 95 is cv2 default

while True:  # send images as stream until Ctrl-C
    image = cam.read()
    # encode image into JPEG format (compressed)
    ret_code, jpg_image = cv2.imencode(".jpg", image, [int(cv2.IMWRITE_JPEG_QUALITY), jpeg_quality])
    sender.send_jpg(rpi_name, jpg_image) # send image

    # if the 'q' or ESC key is pressed, stop the loop
    key = cv2.waitKey(1) & 0xFF
    if key == 27 or key == ord("q"):
        break

    time.sleep(0.1)  # set frame rate

# close the connection
sender.close()
