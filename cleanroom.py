import schedule
import time
import cv2
import os
from pyHS100 import SmartStrip
import argparse

# Set up command line args
parser = argparse.ArgumentParser("Cleanliness Check")
parser.add_argument("-t", "--test", help="Cleanliness check example run is executed with clean image 0 or dirty 1", type=int)
parser.add_argument("-i", "--image", help="Specify the image to use", type=str)
parser.add_argument("-o", "--once", help="Add this option to run the check just once", action='store_true')
args = parser.parse_args()

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
    # Convert image to grayscale
    # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Save image
    # cv2.imwrite('/home/learner/Cleanroom/current_state.jpg', gray)
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

    # Init values
    messy = 0
    clean = 0
    # Each of these commands represents different trained models that can be used
    # to analyze the images

    # First model, pictures colored
    # myCmd = 'python3 ./tensorflow/label_image.py --graph=./tensorflow/room.pb ' \
             # + '--labels=./tensorflow/room.txt --input_layer=Placeholder ' \
             # + '--output_layer=final_result ' \
             # + '--image=/home/learner/Cleanroom/current_state.jpg > out.txt'

    # Grayscale images 
    # myCmd = 'python3 ./tensorflow/label_image.py --graph=./tensorflow/gray.pb ' \
            # + '--labels=./tensorflow/gray.txt --input_layer=Placeholder ' \
            # + '--output_layer=final_result ' \
            # + '--image=/home/learner/Cleanroom/current_state.jpg > out.txt'

    # Dark images removed from clean directory and updated model used
    myCmd = 'python3 ./tensorflow/label_image.py --graph=./tensorflow/room2.pb ' \
            + '--labels=./tensorflow/room2.txt --input_layer=Placeholder ' \
            + '--output_layer=final_result ' \
            + '--image=/home/learner/Cleanroom/current_state.jpg > out.txt'

    # Slightly messy room images removed from set
    # myCmd = 'python3 ./tensorflow/label_image.py --graph=./tensorflow/refined.pb ' \
            # + '--labels=./tensorflow/refined.txt --input_layer=Placeholder ' \
            # + '--output_layer=final_result ' \
            # + '--image=/home/learner/Cleanroom/current_state.jpg > out.txt'
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
    '''
    Checks the current state of the room. The current_state.jpg
    file in the base directory is the imaged that is analyzed.
    The smart plug is turned on or off based on the values.
    '''
    # Determine what image to used based on input args
    if (args.image is not None):
        cmd = 'cp -f ' + args.image + ' current_state.jpg'
        os.system(cmd)
    elif(args.test == 0):
        os.system('cp -f clean.jpg current_state.jpg')
    elif(args.test == 1):
        os.system('cp -f dirty.jpg current_state.jpg')
    else: 
        take_picture()
    # Get the current room state
    messy, clean = get_room_state()
    # Actuate TV based on results
    if messy > clean:
        print('Room messy turning OFF TV')
        plug.turn_off(index=1)
    else:
        print('Room clean turning ON TV')
        plug.turn_on(index=1) 
    

# Determine if we should run just once or multiple times
if(args.once == False):
    # Set schedule for checking the room
    print('Scheduled to run every hour')
    schedule.every().hour.do(roomcheck)
    # This will run the scheduled roomcheck throughout the day.
    while True:                      
        schedule.run_pending()
else:
    roomcheck()
