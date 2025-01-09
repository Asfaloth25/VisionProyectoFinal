from typing import List
import numpy as np
import imageio
import cv2
import copy
import glob
import os
from os.path import join, dirname



import cv2
import imageio
from picamera2 import Picamera2

def write_image(img, path):
    cv2.imwrite(path, img)


imgs = []

def stream_video():
    picam = Picamera2()
    picam.preview_configuration.main.size=(1280, 720)
    picam.preview_configuration.main.format="RGB888"
    picam.preview_configuration.align()
    picam.configure("preview")
    picam.start()


    i = 0
    while True:
        frame = picam.capture_array()
        cv2.imshow("picam", frame)
        if cv2.waitKey(1) & 0xFF == ord('f'):
            imgs.append(frame)
            cv2.imwrite(f'calibration_images/image_{i}.png', frame)
            i += 1
            if i >= 10:
                break
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()


def show_image(img, title='image'):
    cv2.imshow(title, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()



def calibrate(imgs:list):
    corners =  [cv2.findChessboardCorners(img, (7, 7)) for img in imgs]
    valid_imgs = [img for img, corner in zip(imgs, corners) if corner[0]]


    imgs_gray = [cv2.cvtColor(valid_imgs[i], cv2.COLOR_RGB2GRAY) for i in range(len(valid_imgs))]
    valid_corners = [corners[i][1] for i in range(len(corners)) if corners[i][0]]
    corners_copy = copy.deepcopy(valid_corners)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.01) # EPS + MAX_ITER, max 30 iterations, 0.01 accuracy(epsilon)
    corners_refined = [cv2.cornerSubPix(i, cor, (7, 7), (-1, -1), criteria) for i, cor in zip(imgs_gray, corners_copy)]


        
    imgs_with_corners = [cv2.drawChessboardCorners(valid_imgs[i], (7, 7), corners_refined[i], True) for i in range(len(valid_imgs))]
    for i in range(len(imgs_with_corners)):
        show_image(imgs_with_corners[i], f'image {i}')
        write_image(imgs_with_corners[i], f'calibration_images/image_corners_{i}.png')




if __name__ == "__main__":
    stream_video()
    print(len(imgs, 'images'))
    calibrate(imgs)