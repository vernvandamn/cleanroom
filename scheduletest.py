import schedule
import time
import cv2

def take_picture():
    '''Take a picture of the current room state
    '''
    cam = cv2.VideoCapture(1)
    return_value, image = cam.read()
    cam.release()
    # Either write image or return it. 
    # cam.imwrite('mid-bar3.png', image)
    return image

# schedule.every(10).minutes.do(job)
# schedule.every().day.at("10:30").do(job)
# schedule.every(5).to(10).minutes.do(job)
# schedule.every().monday.do(job) 
# schedule.every().wednesday.at("13:15").do(job)  
# schedule.every().minute.at(":17").do(job) 

def current_room_state():
    '''
    Determine the current state of the room by analyzing
    the current picture with the ML algorithm.
    '''
    print("I'm working...")


schedule.every().hour.do(job)

# This will run the scheduled job throughout the day.
while True:                      
    schedule.run_pending()
    time.sleep(1)
