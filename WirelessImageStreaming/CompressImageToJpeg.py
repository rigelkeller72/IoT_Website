# import the necessary packages
import sys
import numpy as np
import cv2
import locale

# grab the reference to the webcam
camera = cv2.VideoCapture(0)

# grab the current frame
(grabbed, image) = camera.read()
cv2.imshow('Original Image', image)
print('Original Image size:   ', "{:,}".format(sys.getsizeof(image)))
orig_size = sys.getsizeof(image)


# keep looping
for jpeg_quality in [90, 70, 50,30,25,20,15,10,5,2.5]:
    
    # encode image into JPEG format (compressed)
    ret_code, jpg_image = cv2.imencode(".jpg", image, [int(cv2.IMWRITE_JPEG_QUALITY), jpeg_quality])
    image2 = cv2.imdecode(np.frombuffer(jpg_image, dtype='uint8'), -1)
    # show the compressed image 
    filename = 'CompressedJpeg_' + str(jpeg_quality)
    cv2.imshow(filename + '  (press key to continue)', image2)

    #print('filename + ' size: ', "{:,}".format(sys.getsizeof(jpg_image)))
    print('%s size: %d (%.1f%s of original size)' %(filename, sys.getsizeof(jpg_image), sys.getsizeof(jpg_image)/orig_size*100, '%'))

    key = cv2.waitKey(0) & 0xFF

key = cv2.waitKey(0) & 0xFF

# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()

