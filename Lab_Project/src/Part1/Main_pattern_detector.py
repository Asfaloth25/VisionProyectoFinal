import corners_detector
from State_machine import Password_state_machine
import cv2
import numpy as np
import copy

from picamera2 import Picamera2

def eval_state(frame:np.array, Harris:bool, PwSM:Password_state_machine):
    _, corners = corners_detector.main(frame,Harris)
    tag = PwSM.get_tag(len(corners))
    tag = PwSM.evaluate(tag)


def stream_video():
    picam = Picamera2()
    picam.preview_configuration.main.size=(1280, 720)
    picam.preview_configuration.main.format="RGB888"
    picam.preview_configuration.align()
    picam.configure("preview")
    picam.start()

    PwSM = Password_state_machine()
    Harris = False

    Password = False
    while not Password:
        frame = picam.capture_array()
        cv2.imshow("picam", frame)
        if cv2.waitKey(1) & 0xFF == ord('h'):
            Harris = True
            eval_state(frame, Harris, PwSM)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            Harris = False
            eval_state(frame, Harris, PwSM)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        if PwSM.current_state == 3:
            Password = True
    
    cv2.destroyAllWindows()