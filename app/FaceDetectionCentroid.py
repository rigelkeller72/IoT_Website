# DetectFace.py
#   This program will detect faces using live video from the default webcam.

# USAGE
# python DetectFace.py

# import the necessary packages (specifically the opencv package)
import cv2
import time
import sqlite3
import pyttsx3
import imagezmq, os
import numpy as np
import sys

sys.path.append('/home/ubuntu/.local/lib')

# # create a video object for the default webcam
# camera = cv2.VideoCapture(0)

# create cascade classifier which uses a face database
face_cascade = cv2.CascadeClassifier('HarrXML\haarcascade_frontalface_alt2.xml')

# Wireless image collection. (Using imagezmq libarary)
Receive_From_Address = 'tcp://127.0.0.1:5001'
image_hub = imagezmq.ImageHub(open_port=Receive_From_Address, REQ_REP=False)

print("Press ESC or q to end program")
frame_number = 0  # this variable is used to count the frames
start_frame_number = 0  # used to count Frames Per Second
start_seconds = time.time()  # used to count Frames Per Second
start_time =time.time()
fps = 0  # used to count Frames Per Second
i = 0

# data base commands
conn = sqlite3.connect("site_data.db")

# initialize the voice engine
#engine = pyttsx3.init()

# keep looping
while True:
    frame_number = frame_number + 1  # count each frame that is processed

    # # grab the current frame
    # (grabbed, img) = camera.read()

    # grab the current frame (WIRELESS)
    host_name, jpg_buffer = image_hub.recv_jpg()
    img = cv2.imdecode(np.frombuffer(jpg_buffer, dtype='uint8'), -1)

    # convert color image to gray scale image (FDcode)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # find faces in entire image (uncomment one) (FDcode)
    faces = face_cascade.detectMultiScale(gray)
    # faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=4)
    # faces = face_cascade.detectMultiScale(gray,scaleactor=1.2, minNeighbors=5, minSize=(100, 100), maxSize=(250, 250))
    # print(faces)
    # print("Size of faces:", len(faces))

    if len(faces) > 0:  # people have been detected
        #print("Face detected")
        # draw retangle around each detected face
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.line(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.line(img, (x, y + h), (x + w, y), (255, 0, 0), 2)
            centroidx = x + w / 2
            centroidy = y + h / 2
            cv2.putText(img, 'Face detected!!', (200, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 2)
            # print("Face: Left=%d Top=%d Width=%d Height=%d" % (x, y, w, h))
            # print("Centroid: %d, %d" % (centroidx, centroidy))

            # send data base face data every 1 second
            if (time.time() - start_seconds) > 5:
                #engine.say('Intruder Alert!')
                #engine.runAndWait()
                # data base commands
                ts = time.time()
                cursor = conn.execute("INSERT INTO faces VALUES (?,?,?)", (centroidx, centroidy, ts,))
                cursor.close()
                conn.commit()
                start_frame_number = frame_number
                start_seconds = time.time()
    #else:

        #print('No faces')

    # if 5 seconds have passed, compute Frames Per Second and SQL insert to data base
    if (time.time() - start_seconds) > 5:
        fps = (frame_number - start_frame_number) / (time.time() - start_seconds)
        # print("Centroid: %d, %d" % (centroidx, centroidy))
        # data base commands
        # cursor = conn.execute("INSERT INTO faces VALUES (?,?,?)", (centroidx, centroidy, frame_number,))
        # cursor.close()
        # conn.commit()
        start_frame_number = frame_number
        start_seconds = time.time()

    # print frame number and Frames Per Second on image
    #cv2.putText(img, str(frame_number), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2)
    #cv2.putText(img, 'FPS: %02.1f' % (fps), (470, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2)


    # resize the frame, optional
    img = cv2.resize(img, (0, 0), fx=2.0, fy=2.0)

    # display image which contains rectangles drawn on it
    savestr = os.getcwd()+"/static/images/test.jpg"
    cv2.imwrite(savestr, img)
    #cv2.imshow("AGAGA",img)

    # check keyboard for a keypress
    key = cv2.waitKey(1) & 0xFF

    # if the ESC or 'q' key is pressed, stop the loop
    if key == 27 or key == ord("q"):
        break

# # cleanup the camera
# camera.release()
# close the connection
image_hub.close()
# close any open windows
cv2.destroyAllWindows()
