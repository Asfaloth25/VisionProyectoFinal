# Real-time movement tracker with external information using Raspberry Pi

## Description:
This project can be separated in to three main modules:
-  The calibration module, which allows the user to calibrate the Raspberry Pi Camera.
-  The security module, that only allows the user to access the rest of the program's functionality once the correct sequence of drawn patterns has been scanned.
-  The main module, which tracks the movement of any object in real time; showing the graph of the temporal evolution of the desired variable: speed or acceleration.

This project is based on [*OpenCV*](https://github.com/opencv/opencv/wiki), and uses [*Matplotlib's interactive graphs*](https://matplotlib.org/stable/users/explain/figure/interactive.html) to render the graphs.

## Main modules
### Calibration module:
Using this program, the user should take 10 images of a checkerbord pattern, from different angles. Then, after these captures have been taken, the camera's intrinsic parameters are shown to the user.
![image_corners_8](https://github.com/user-attachments/assets/d0d7076a-d28f-41ad-8f40-753574385f84)



### Security module:
When executed, the [*Picamera2*](https://datasheets.raspberrypi.com/camera/picamera2-manual.pdf) library starts capturing live video from the Raspberry Pi. The video is displayed on a window.
In this state, the program expects the user to take a sequence of captures of patterns, in order to be granted access to the main module. This is achieved by pressing a key once
the pattern is shown to the camera. The user can choose the detection algorithm to employ: either Harris or Shi Tomasi (_After thorough experimentation, the latter one is more consistant, and thus reccommended_).

Once the user chooses one of these algorithms, another window will pop up and show the output of the detection algorithm. Here are two separate examples for different patterns:

![20250108_11h47m23s_grim](https://github.com/user-attachments/assets/7562dbfd-a68d-48c6-8ce9-94e28a7704cb)


![20250108_11h56m30s_grim](https://github.com/user-attachments/assets/4dc2133c-7d54-4338-808f-f45388e675f3)


The user may now proceed to the next step using this image or, on the contrary, repeat the capture.

Currently, for the sake of simplicity, the password has three digits, so the user will have to repeat this process twice.
The detection algorithm is based on a State Machine, and will determine whether this shape corresponds to the current digit in the password. If so, it will proceed to the next digit, until the password is complete and correct.


### Main module:
This program will start displaying the real-time recording of the Picamera once it is launched. Once the camera is still and facing the right way, the user can press a key to start the tracking. 
The user can now choose which metric to display in the graph: velocity or accelleration.

Once the choice is made, the moving object will be tracked in real time. Additionally, an auxiliary window will emerge, with a graph of the selected metric. This graph will also be updated in real time.

Sometimes, static points in the image will be tracked by error. However, they will be regarded as outliers, and will not be taken in to account when calculating the speed and accelleration of the moving object.


https://github.com/user-attachments/assets/3d00dbb9-2108-420b-979c-5de1cf614594


In this video demonstration, the camera was placed upside-down for stability purposes. However, the most remarkable aspects that can be noted from it are:
- In this test, the video and graph have a **refresh rate of 30 frames per second**. Although the program had proved to work at 50 fps, we decided to limit it because the RPi started heating noticeably at that higher framerate.
- The graph shows the temporal evolution of the student's velocity. When he moves to the right on the image (his left), the graph shows a value above 0. When moving to the left, the value is negative. When standing still, the value is approximately 0.
- The first seconds of the video show a very noisy graph. This noise is various orders of magnitude smaller than the values shown when moving (as you can see, when the student starts moving, the noise is so small in comparison it fades away). This noise can be attributed to minor movements in the image and its target.

## Application to real-life problems
We believe this program, with some modifications, can be deployed on a wide range of situations:
- In a highway radar, to track the speed of incoming cars.
- In sports: to calculate the speed and accelleration of players, tennis serves or golf swings.
- In mechanized production, to monitor the correct functioning of manufacturing robots.
