import cv2
import imagezmq

# open sender with IP address to send to
sender = imagezmq.ImageSender(connect_to='tcp://192.168.1.3:5555')

# create any name for this computer
rpi_name = 'RasPi 1'  # send RasPi name with each image

# open the webcam
cam = cv2.VideoCapture(0)

while True:

    # read image from camera
    (grabbed, image) = cam.read()

    # send image and sender's name
    sender.send_image(rpi_name, image) 
