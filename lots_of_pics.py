import cv2
import numpy as np
import schedule
import time

def take_picture():
    # Set up video capture
    cam = cv2.VideoCapture(1)
    # cam.set(cv2.CAP_PROP_FRAME_COUNT, 5)
    # cam.set(3, 640)
    # cam.set(4, 480)
    # Get image
    return_value, image = cam.read()
    # Set file name to save image to
    current_time = time.strftime("%d_%H-%M-%S")
    filepath = './pics/' + current_time + '.png'
    print(filepath)
    # Save image
    cv2.imwrite(filepath, image)
    # Release camera
    cam.release()
    # Finished
    print('pic taken')

take_picture()
#Run once
schedule.every(15).seconds.do(take_picture)

while True:
    # Run scheduled
    try:
        schedule.run_pending()
    except(KeyboardInterrupt, SystemExit):
        raise
    except:
        print('CV2 error occured')
