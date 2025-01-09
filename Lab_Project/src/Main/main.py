from Lab_Project.src.Security.Main_pattern_detector import security_sequence
from Lab_Project.src.Tracking.opticalflow import stream_video

def main():
    password_correct = security_sequence()
    if password_correct:
        stream_video()
    else:
        print('Incorrect password! Ending execution...')

if __name__ == '__main__':
    main()