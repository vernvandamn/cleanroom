import schedule
import time
import cv2
import os
from pyHS100 import SmartStrip
import argparse

# Set up command line args
parser = argparse.ArgumentParser("Cleanliness Check")
parser.add_argument("test", help="Cleanliness check example run is executed with clean image 0 or dirty 1", type=int)

# Set up smartplug connection
plug = SmartStrip("192.168.1.131")

def take_picture():
    '''Take a picture of the current room state
    '''
    print('Taking picture of room')
    # Turn on light before image is taken
    plug.turn_on(index=0) 
    # Initialize camera
    cam = cv2.VideoCapture(1)
    # Get image
    return_value, image = cam.read()
    cam.release()
    # Save image
    cv2.imwrite('/home/learner/Cleanroom/current_state.jpg', image)
    plug.turn_off(index=0)


def get_room_state():
    '''
    Determine the current state of the room by analyzing
    the current picture with the ML algorithm.
    '''
    print("\nAnalyzing image...\n")
    # Kernal kills my process when I try and redirect the stderr to 
    # /dev/null. Instead of messing with timeout limits I'll just let
    # it do it's thing.
    messy = 0
    clean = 0
    myCmd = 'python3 ./tensorflow/label_image.py --graph=./tensorflow/room.pb ' \
            + '--labels=./tensorflow/room.txt --input_layer=Placeholder ' \
            + '--output_layer=final_result ' \
            + '--image=/home/learner/Cleanroom/current_state.jpg > out.txt'
    os.system(myCmd)
    with open("out.txt") as results:
        data = results.readlines()
        messy = float(data[0].split()[1])
        clean = float(data[1].split()[1])

    # Print values
    print('\n\nMessy score: ' + str(messy))
    print('Clean score: ' + str(clean))
    # Remove log file
    os.system('rm out.txt')
    return messy, clean


def roomcheck():
    args = parser.parse_args()
    if(args.test == 0):
        os.system('cp -f clean.jpg current_state.jpg')
    else if(args.test == 1):
        os.system('cp -f dirty.jpg current_state.jpg')
    else: 
        take_picture()

    messy, clean = get_room_state()
    if messy > clean:
        print('Room messy turning OFF TV')
        plug.turn_off(index=1)
    else:
        print('Room clean turning ON TV')
        plug.turn_on(index=1) 
    

# Select schedule for checking the room
# schedule.every(10).minutes.do(roomcheck)
# schedule.every().day.at("10:30").do(roomcheck)
# schedule.every(5).to(10).minutes.do(roomcheck)
# schedule.every().monday.do(roomcheck) 
# schedule.every().wednesday.at("13:15").do(roomcheck)  
# schedule.every().minute.at(":17").do(roomcheck) 
# schedule.every().hour.do(roomcheck)
roomcheck()

# This will run the scheduled roomcheck throughout the day.
while True:                      
    schedule.run_pending()
