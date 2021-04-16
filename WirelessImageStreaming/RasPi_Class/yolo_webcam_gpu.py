# USAGE
# python yolo_video.py

# import the necessary packages
import numpy as np
import imutils
import cv2
import imagezmq

YOLO_confidence_level=0.5
YOLO_threshold_level=0.3

print('Loading YOLO Deep Neural Network trained on COCO image set')

# load the COCO class labels our YOLO model was trained on
LABELS = open('yolo-coco\coco.names').read().strip().split("\n")

# initialize a list of colors to represent each possible class label
np.random.seed(42)
YOLO_COLORS = np.random.randint(0, 255, size=(len(LABELS), 3),
    dtype="uint8")

# load our YOLO object detector trained on COCO dataset (80 classes)
net = cv2.dnn.readNetFromDarknet('yolo-coco\yolov3.cfg', 'yolo-coco\yolov3.weights')
ln = net.getLayerNames()
ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]
#--------------------
# Set the backend target to use CUDA-enabled GPU
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
print('Using GPU enabled OpenCV')
#--------------------

Receive_From_Address = 'tcp://192.168.1.3:5555' #'tcp://10.60.81.246:5555'

image_hub = imagezmq.ImageHub(open_port=Receive_From_Address, REQ_REP=False)

# record frame dimensions
host_name, jpg_buffer = image_hub.recv_jpg()
frame = cv2.imdecode(np.frombuffer(jpg_buffer, dtype='uint8'), -1)
(H, W) = frame.shape[:2]
    
ii=1
# loop over frames from the video file stream
while True:
    # grab the current frame
    host_name, jpg_buffer = image_hub.recv_jpg()
    frame = cv2.imdecode(np.frombuffer(jpg_buffer, dtype='uint8'), -1)


    # construct a blob from the input frame and then perform a forward
    # pass of the YOLO object detector, giving us our bounding boxes
    # and associated probabilities
    blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416),
        swapRB=True, crop=False)
    net.setInput(blob)
    layerOutputs = net.forward(ln)

    # initialize our lists of detected bounding boxes, confidences,
    # and class IDs, respectively
    boxes = []
    confidences = []
    classIDs = []

    # loop over each of the layer outputs
    for output in layerOutputs:
        # loop over each of the detections
        for detection in output:
            # extract the class ID and confidence (i.e., probability)
            # of the current object detection
            scores = detection[5:]
            classID = np.argmax(scores)
            confidence = scores[classID]

            # filter out weak predictions by ensuring the detected
            # probability is greater than the minimum probability
            if confidence > YOLO_confidence_level:
                # scale the bounding box coordinates back relative to
                # the size of the image, keeping in mind that YOLO
                # actually returns the center (x, y)-coordinates of
                # the bounding box followed by the boxes' width and
                # height
                box = detection[0:4] * np.array([W, H, W, H])
                (centerX, centerY, width, height) = box.astype("int")

                # use the center (x, y)-coordinates to derive the top
                # and and left corner of the bounding box
                x = int(centerX - (width / 2))
                y = int(centerY - (height / 2))

                # update our list of bounding box coordinates,
                # confidences, and class IDs
                boxes.append([x, y, int(width), int(height)])
                confidences.append(float(confidence))
                classIDs.append(classID)

    # apply non-maxima suppression to suppress weak, overlapping
    # bounding boxes
    idxs = cv2.dnn.NMSBoxes(boxes, confidences, YOLO_confidence_level,YOLO_threshold_level)

    # ensure at least one detection exists
    if len(idxs) > 0:
        # loop over the indexes we are keeping
        for i in idxs.flatten():
            # extract the bounding box coordinates
            (x, y) = (boxes[i][0], boxes[i][1])
            (w, h) = (boxes[i][2], boxes[i][3])

            # draw a bounding box rectangle and label on the frame
            color = [int(c) for c in YOLO_COLORS[classIDs[i]]]
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            text = "{}: {:.1f}".format(LABELS[classIDs[i]],
                confidences[i]*100)
            cv2.putText(frame, text, (x, y - 5),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        # resize the frame, optional 
        frame = cv2.resize(frame, (0,0), fx=2.0, fy=2.0)

        # show the frame to our screen and increment the frame 
        cv2.imshow("YOLO Deep NNET", frame)

        # if the 'q' key is pressed, stop the loop
        key = cv2.waitKey(1) & 0xFF
        if key == 27 or key == ord("q"):
                break
        
#        print('Processed frame: ', ii)
    ii=ii+1

print("Cleaning up...")
# close the connection
image_hub.close()
# close any open windows
cv2.destroyAllWindows()

