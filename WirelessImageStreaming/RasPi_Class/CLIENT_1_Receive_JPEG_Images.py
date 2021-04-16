#Host must be running before executing this program

import numpy as np
import cv2
import imagezmq

Receive_From_Address = 'tcp://192.168.4.1:5555' #'tcp://10.60.81.246:5555'

image_hub = imagezmq.ImageHub(open_port=Receive_From_Address, REQ_REP=False)

print('CLIENT 1 receiving images from ' + Receive_From_Address)
print('Press q to end program.')
while True:  # press Ctrl-C to stop image display program
    host_name, jpg_buffer = image_hub.recv_jpg()
    image = cv2.imdecode(np.frombuffer(jpg_buffer, dtype='uint8'), -1)

    # resize the frame, optional 
    #image = cv2.resize(image, (0,0), fx=2.0, fy=2.0)

    cv2.imshow(host_name, image)

    # if the 'q' key is pressed, stop the loop
    key = cv2.waitKey(1)
    if key == 27 or key == ord("q"):
        break

# close the connection
image_hub.close()
# close any open windows
cv2.destroyAllWindows()
