# pip install opencv-python

from cv2 import *
import time

cam_port = 0 # Try changing this if it doesn't work

def main():
    cam = VideoCapture(cam_port)

    for i in range(10):
        result, image = cam.read()
        imwrite(f"Data/Output_{i}.tiff", image)
        time.sleep(0.5) # sleep for 500ms

if __name__ == "__main__":
    main()
