import cv2
import numpy as np
import time
from robot_control import *
import keyboard
import threading
import os

def robot_task():
    move_robot(*robot_positions['work_position'])
    move_robot(*robot_positions['home_position'])
    move_robot(*robot_positions['work_position'])
    x, y = get_robot_cords((175, 175))
    move_robot(x, y, -0.10, 90)
    move_robot(*robot_positions['work_position'])
    move_robot(*robot_positions['home_position'])
    os._exit(0)

def check_for_stop_key():
    while True:
        if keyboard.is_pressed('shift'):
            robot.stop()
            os._exit(0)
            break
        time.sleep(0.01)


robot_thread = threading.Thread(target=robot_task)
key_thread = threading.Thread(target=check_for_stop_key)

robot_thread.start()
key_thread.start()

robot_thread.join()
key_thread.join()

