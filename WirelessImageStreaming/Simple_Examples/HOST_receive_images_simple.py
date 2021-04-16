""" receive_images_simple.py -- receive & display image stream.

A simple test program that uses imagezmq to receive an image jpg stream from a
Raspberry Pi and display it as a video steam.

1. Run this program first on windows:
python receive_images_simple.py

This "receive and display images" program must be running before starting the
RasPi sending program.

2. Run the sending program on the RPi:
python send_images_simple.py

A cv2.imshow() window will appear on the PC showing the tramsmitted images as
a video stream. You can repeat Step 2 and start the send_images_simple.py on
multiple RasPis and each one will cause a new cv2.imshow() window to open.

To end the programs, press Ctrl-C in the terminal window of the RasPi first.
Then press "q" in the display window of the receiving proram. You may have 
to press Ctrl-C in the terminal window as well.
"""

import cv2
import imagezmq

# open image hub
image_hub = imagezmq.ImageHub()

while True: 

    # get image from hub
    sender_name, image = image_hub.recv_image()

    # display image
    cv2.imshow(sender_name, image)
    
    # acknowledge image was received
    image_hub.send_reply(b'OK')

    # pause to allow image to display
    cv2.waitKey(1)



