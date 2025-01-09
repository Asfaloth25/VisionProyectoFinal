from typing import List
import numpy as np
import imageio
import cv2
import copy
import glob
import os
from os.path import join, dirname

import imageio

def show_image(img, title='image'):
    cv2.imshow(title, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def write_image(img, path):
    cv2.imwrite(path, img)


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


def main():
    calibration_imgs_path = 'calibration_images'
    imgs = [cv2.imread(f'{calibration_imgs_path}/image_{i}.png') for i in range(10)]
    calibrate(imgs)


if __name__ == '__main__':
    main()

