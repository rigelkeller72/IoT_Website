# USAGE
# python TestWebCam.py

# import the necessary packages
import cv2

# grab the reference to the webcam
camera = cv2.VideoCapture(0)

# keep looping
while True:
    # grab the current frame
    (grabbed, frame) = camera.read()

    #    # resize the frame, optional
    #    frame = cv2.resize(frame, (0,0), fx=2.0, fy=2.0)

    # show the frame to our screen and increment the frame
    cv2.imshow("Test Webcam", frame)

    # if the 'q' key is pressed, stop the loop
    key = cv2.waitKey(1) & 0xFF
    if key == 27 or key == ord("q"):
        break

# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()


