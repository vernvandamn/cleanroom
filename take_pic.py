import cv2

cam = cv2.VideoCapture(1)
return_value, image = cam.read()
cv2.imwrite('current_state.jpg', image)
cam.release()
