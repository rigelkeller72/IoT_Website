#DetectFace.py
#   This program will detect faces using live video from the default webcam.

# USAGE
# python DetectFace.py 

# import the necessary packages (specifically the opencv package)
import cv2
import time

# create a video object for the default webcam
camera = cv2.VideoCapture(1)
 
# create cascade classifier which uses a face database
face_cascade = cv2.CascadeClassifier('HarrXML\haarcascade_frontalface_alt2.xml')

print("Press ESC or q to end program")
frame_number=0; # this variable is used to count the frames
start_frame_number = 0
start_seconds = time.time()
fps=0
# keep looping
while True:
    frame_number=frame_number+1 # count each frame that is processed
    
    # grab the current frame
    (grabbed, img) = camera.read()

    # convert color image to gray scale image
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # find faces in entire image (uncomment one)
    faces = face_cascade.detectMultiScale(gray)
    #faces = face_cascade.detectMultiScale(gray,scaleFactor=1.1,minNeighbors=10)
    #faces = face_cascade.detectMultiScale(gray,scaleFactor=1.1,minNeighbors=10,minSize=(100, 100),maxSize=(200, 200))

    # draw retangle around each detected face
    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        #print("Face: Left=%d Top=%d Width=%d Height=%d" % (x, y, w, h))
    
    if (time.time() - start_seconds) > 5:
        fps= (frame_number - start_frame_number) / (time.time() - start_seconds)
        start_frame_number = frame_number
        start_seconds = time.time()

    # print frame number and frame rate on image
    cv2.putText(img, str(frame_number), (10, 30), cv2.FONT_HERSHEY_SIMPLEX,1.0, (0, 255, 0), 2)
    cv2.putText(img, 'FPS: %02.1f' %(fps), (470, 30), cv2.FONT_HERSHEY_SIMPLEX,1.0, (0, 255, 0), 2)
 
    # resize the frame, optional 
    img = cv2.resize(img, (0,0), fx=2.0, fy=2.0)

        # display entire image which contains rectangles drawn on it 
    cv2.imshow("Face Detector", img)
    
    
    # check keyboard for a keypress
    key = cv2.waitKey(1) & 0xFF

    # if the ESC or 'q' key is pressed, stop the loop
    if key == 27 or key == ord("q"):
        break

# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()
