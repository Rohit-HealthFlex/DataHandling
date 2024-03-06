from src.utilities.utils import calculate_rot_angle
import numpy as np


class Presets:
    def __init__(self):
        self.direction = {"z": ["top", "down", ""],
                          "y": ["left", "right", ""],
                          "x": ["front", "back", ""]}
        self.angle_hold = []
        self.xyz_angle_hold = [] #used to hold roll pitch yaw values

    def get_direction(self, rot_info):
        dir_vals = []
        rot_x, rot_y, rot_z = rot_info
        x_flag = rot_x < 180
        if rot_x == 0:
            x_flag = -1
        dir_vals.append(self.direction["x"][x_flag])

        y_flag = rot_y > 180
        if rot_y == 0:
            y_flag = -1
        dir_vals.append(self.direction["y"][y_flag])

        z_flag = rot_z > 180
        if rot_z == 0:
            z_flag = -1
        dir_vals.append(self.direction["z"][z_flag])

        return dir_vals

    def get_angle(self, angle_info):
        if len(angle_info) != 2:
            return
        sensor0_rot = angle_info[0][1]["rot"]
        sensor1_rot = angle_info[1][1]["rot"]
        out = calculate_rot_angle(sensor0_rot, sensor1_rot)
        self.angle_hold.append(out)
        #print(self.angle_hold[0])
        return out

    def get_position(self, pos_info):
        if len(pos_info) != 3:
            return
        return {"x": pos_info[0],
                "y": pos_info[1],
                "z": pos_info[2]}
    
    def get_distance(self, pos_info):
        if len(pos_info) != 3:
            return
        p1 = np.array([0, 0, 0])
        p2 = np.array([pos_info[0], pos_info[1], pos_info[2]])
        squared_dist = np.sum((p1-p2)**2, axis=0)
        dist = np.sqrt(squared_dist)
        return dist
"""     
    def angle_bn_sensor(self, xyz_angle_info):
        if len(xyz_angle_info) != 3:
            return
         """

"""     
    def check_starting_position(self):
        
"""
