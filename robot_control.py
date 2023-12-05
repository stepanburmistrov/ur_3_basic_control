import urx
from urx.robotiq_two_finger_gripper import Robotiq_Two_Finger_Gripper

import time
import numpy as np
import math3d as m3d
import math


class Nedorobot:
    def __init__(self,ip):
        self.ip = ip
    def getl(self):
        print('nedorobot_ok')
    def movel(self,coord,a,b,wait='0'):
        print('go to', self.ip, coord)

class Nedogripper:
    def __init__(self, robot_id):
        print('nedogrip_ok')
    def gripper_action(self,angle):
        print('gripper goto', angle)

try:
    robot = urx.Robot('192.168.2.175')
    grip = Robotiq_Two_Finger_Gripper(robot)
except Exception as e:
    robot = Nedorobot('left_robot')
    grip = Nedogripper(robot)
    print('right robot is Nedorobot', e)

state= robot.getl()
print(state)

robot_positions = {'work_position': [-0.300, 0.10, 0.000, 90],
                   'home_position': [-0.140, 0.106, 0.190, 90],
                   }

def angle_gripper(angle):
    angle = 90 - angle - 0.01
    roll = 0
    pitch = 3.14
    yaw = np.deg2rad(angle)

    yawMatrix = np.matrix([
        [math.cos(yaw), -math.sin(yaw), 0],
        [math.sin(yaw), math.cos(yaw), 0],
        [0, 0, 1]
    ])

    pitchMatrix = np.matrix([
        [math.cos(pitch), 0, math.sin(pitch)],
        [0, 1, 0],
        [-math.sin(pitch), 0, math.cos(pitch)]
    ])

    rollMatrix = np.matrix([
        [1, 0, 0],
        [0, math.cos(roll), -math.sin(roll)],
        [0, math.sin(roll), math.cos(roll)]
    ])

    R = yawMatrix * pitchMatrix * rollMatrix

    theta = math.acos(((R[0, 0] + R[1, 1] + R[2, 2]) - 1) / 2)
    multi = 1 / (2 * math.sin(theta))

    rx = multi * (R[2, 1] - R[1, 2]) * theta
    ry = multi * (R[0, 2] - R[2, 0]) * theta
    rz = multi * (R[1, 0] - R[0, 1]) * theta
    rz = 0

    return rx, ry, rz

def get_robot_cords(x_y):
    robot_coords = []
    x, y = x_y[0], x_y[1]
    y_r = x - 325
    x_r = y - 450
    robot_coords.append(x_r / 1000)
    robot_coords.append(y_r / 1000)
    return robot_coords

def move_robot(x, y, z, angle, w=True):
    rx, ry, rz = angle_gripper(angle)
    robot.movel([x, y, z, rx, ry, rz], 0.05, 0.05, wait=w)
