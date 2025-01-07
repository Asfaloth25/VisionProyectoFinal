import cv2
import imageio
from picamera2 import Picamera2
import copy
import numpy as np
import time

from embed_graph import embed_graph_on_image

### Configuración del flujo óptico
winSize=(15, 15)
maxLevel=2
criteria= (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03)

def stream_video():
    picam = Picamera2()
    picam.preview_configuration.main.size=(640, 360) #1280, 720)
    picam.preview_configuration.main.format="RGB888"
    picam.preview_configuration.align()
    picam.configure("preview")
    picam.start()


    i = 0
    recording = False
    frames = []
    delta_time = time.time()
    fps = 10
    median_speed_new = [0,0]
    while True:
        delta_time = time.time() - delta_time
        if delta_time <= 1/fps:
            time.sleep(1/fps - delta_time)


        frame = picam.capture_array()

        frame_height, frame_width, _ = frame.shape
        if recording:
            frames.append(frame)

            input_frame = copy.copy(frame)
            frame_gray = cv2.cvtColor(input_frame, cv2.COLOR_BGR2GRAY)
            p1, st, err = cv2.calcOpticalFlowPyrLK(prev_gray, frame_gray, p0, None, winSize=winSize, maxLevel=maxLevel, criteria=criteria)
            if p1 is not None and st is not None:
                good_new = p1[st == 1]
                good_old = p0[st == 1]
                # Draw the tracks
                for new, old in zip(good_new, good_old):
                    a, b = new.ravel().astype(int)
                    c, d = old.ravel().astype(int)
                    input_frame = cv2.circle(input_frame, (a, b), 5, (0, 0, 255), -1)  # Draw current point in red
                    mask = cv2.line(mask, (a, b), (c, d), (0, 255, 0), 2)  # Draw line in green
                # Updating the inputs for the next iteration
                prev_gray = frame_gray.copy()  # Copy the current frame to the previous frame
                p0 = good_new.reshape(-1, 1, 2)  # Update the points to track
        
                frame_with_flow = cv2.add(input_frame, mask) - background_image

                # SPEED CHECK
                optical_flow_points = np.array(good_new) - np.array(good_old)
                print(optical_flow_points)
                sorted_flows = sorted(optical_flow_points, key = lambda x: sum(x**2)) # the speed of each point, sorted by euclidean distance to the origin (length)
                median_speed_old = median_speed_new
                median_speed_new = sorted_flows[len(sorted_flows)//2] # the median speed of the interest points
                delta_speed = median_speed_new-median_speed_old
                

                print('Median:', median_speed_new)
        cv2.imshow("picam", frame if not recording else frame_with_flow)
        if cv2.waitKey(1) & 0xFF == ord('f'):
            cv2.imwrite(f'calibration_images/image_{i}.png', frame)
            i += 1
            if i >= 10:
                break
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print('EXECUTION TERMINATED')
            break
        if cv2.waitKey(1) & 0xFF == ord('s'):
            recording = True
            background_image = frame
            print('RECORDING STARTED')
            frame = picam.capture_array()
            frames.append(frame)

            #TODO: Convert the first frame to grayscale
            prev_gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

            #TODO: Define the parameters of the Shi-Tomasi algorithm
            mask=None
            maxCorners = 100
            qualityLevel = 0.3
            minDistance = 7
            blockSize = 7
            mask = np.zeros_like(frame)

            # Use the function goodFeaturesToTrack to detect the points of interest
            p0 = cv2.goodFeaturesToTrack(prev_gray, mask=mask, maxCorners=maxCorners, qualityLevel=qualityLevel, minDistance=minDistance, blockSize=blockSize)
            mask = np.zeros_like(frame)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    stream_video()