# Cleanroom

## How to use

To run the script, from the base directory, type
``
python3 cleanroom.py -o -t 0
``
The -o option runs the script just once and doesn't schedule repeated checks.
The -t 0 option runs the script with a test image of a clean room. Replacing the 0 with
a 1 tests the script with a messy room. 
A -i option can also be provided to test the output against a picture specified by the full
path to the picture(e.g. -i /home/learner/pics/image.jpg)

If the tensorflow folder does not contain the necessary .pb or .txt files the model must be 
retrained by using the following script(script was obtained from [github](https://github.com/tensorflow/hub/raw/r0.1/examples/image_retraining/retrain.py):
``
python3 retrain.py \
	--image_dir /home/learner/Cleanroom/pics \
 	--output_graph=room.pb \
 	--output_labels=room.txt \
 	--tfhub_module https://tfhub.dev/google/imagenet/inception_v3/feature_vector/3
``

The image is then run through the model by using a call to the following script also acquired
from [tensorflow's github](https://github.com/tensorflow/tensorflow/raw/master/tensorflow/examples/label_image/label_image.pyh):
``
python label_image.py \
    --graph=rooms.pb \
    --labels=rooms.txt \
    --input_layer=Placeholder \
    --output_layer=final_result \
    --image=/path/to/new_image.jpg
``

## Idea
The goal is to actuate a smartplug depending on the cleanliness of the room. This is to be
accomplished by retraining a image classification model with images of a clean and messy
room and depending on the output of the analysis of the image a smart plug connected to
the TV is turned on or off. 

The idea was conceived by Matt Farley and his idea was posted here on [hackster.io](https://www.hackster.io/matt-farley/use-artificial-intelligence-to-detect-messy-clean-rooms-f224a2#toc-step-5---integrate-and-put-your-model-to-work-5)

## Implementation

### 
Notes from the project collected in  OneNote exported to a pdf are included in the 
Cleanroom folder

### Collect data
To collect the data I setup a webcam that would take pictures every 30 seconds for a
few days. A good number of these had the floor obscured or were too dark to use. 
Sifting through the data to find the images that were obviously clean or dirty took a lot
of time.

I used the python script `lots_of_pics.py` located in the base directory to get the pictures

### Train and test script
The model retrained against the images produces values that indicate the likelihood of the 
object in the image. 

### Results
The models didn't seem to produce the results I was looking for. I tried retraining a few
different models, but none of the other models I tried would successfully retrain on the
device. Either the process ran out of memory or the process was killed by the kernel by a
reason I'm not sure of. 

I don't know if there just wasn't enough images to produce a good
enough re-training set or if there were other issues with the subject that complicated the
matter. The light differences in the room might have thrown of the values. Running the script
on a bedroom where there might be more consistent lighting could help.

The best results were obtained by placing a light on the floor that would turn on while the 
image was obtained. The long shadows had a consistent effect on the clean value. The other
values varied too much depending on the light in the room or the position of the debris to
rely on. 

## Possible Paths Forward
I could possibly break the image of the entire floor up into sections and running the 
smaller sections against the classification model might produce better results. This would
increase the time per evaluation but that isn't really a restriction in the current setup.

More images would probably help produce more accurate results. If I retrained the model using
weeks worth of data the values would probably come out more correct. 

It might be possible to use background subtraction and webcam video to remove the background
and work with images of the debris by itself.
