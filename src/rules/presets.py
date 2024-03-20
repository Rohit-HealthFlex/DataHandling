from src.utilities.utils import calculate_rot_angle
from src.utilities.utils import get_eulirean_angles
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
        x_flag = rot_x > 180
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
        if len(angle_info) != 2: # Was 2
            return
        sensor0_rot = angle_info[0][1]["rot"]
        sensor1_rot = angle_info[1][1]["rot"]
        out = calculate_rot_angle(sensor0_rot, sensor1_rot)
        #sensor0_pos = pos_info[0][1]["pos"]
        #print(sensor0_pos)
        #sensor1_pos = pos_info[1][1]["pos"]
        #print(sensor1_pos)
        #alpha, beta, gamma = get_eulirean_angles(sensor0_rot, sensor1_rot, sensor0_pos, sensor1_pos)
        #out = [alpha, beta, gamma]
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

    def get_starting_pos(self, angle_info):
        if len(angle_info) != 2:
            return
        
        # Sitting
        if (# Check shin x angle
            ((340 < angle_info[1][1]["ang"][0] < 360) or (0 <= angle_info[1][1]["ang"][0] < 20)) 
            
            # Check shin y angle
            and ((340 < angle_info[1][1]["ang"][1] < 360) or (0 <= angle_info[1][1]["ang"][1] < 20)) 
            
            # Check thigh x angle
            and (240 <= angle_info[0][1]["ang"][0] <= 280) 
            
            # Check thigh y angle
            and ((0 <= angle_info[0][1]["ang"][1] < 20) or (340 < angle_info[0][1]["ang"][1] < 360))
            ):

            return "sitting"
        
        # Standing
        elif (((345 < angle_info[1][1]["ang"][0] < 360) or (0 <= angle_info[1][1]["ang"][0] < 15)) 
              and ((345 < angle_info[1][1]["ang"][1] < 360) or (0 <= angle_info[1][1]["ang"][1] < 15))
              and ((345 < angle_info[0][1]["ang"][0] < 360) or (0 <= angle_info[0][1]["ang"][0] < 15))
              and ((345 < angle_info[0][1]["ang"][1] < 360) or (0 <= angle_info[0][1]["ang"][1] < 15))
              ):
            
            return "standing"
        
        # Supine
        elif ((260 < angle_info[1][1]["ang"][0] < 280)
              and ((350 < angle_info[1][1]["ang"][1] < 360) or (0 <= angle_info[1][1]["ang"][1] < 10))
              and (260 <= angle_info[0][1]["ang"][0] < 280)
              and ((350 < angle_info[0][1]["ang"][1] < 360) or (0 <= angle_info[0][1]["ang"][1] < 10))
              ):
            
            return "supine"
        
        # Prone
        elif ((80 < angle_info[1][1]["ang"][0] < 100)
              and ((345 < angle_info[1][1]["ang"][1] < 360) or (0 <= angle_info[1][1]["ang"][1] < 15))
              and (80 < angle_info[0][1]["ang"][0] < 100)
              and ((345 < angle_info[0][1]["ang"][1] < 360) or (0 <= angle_info[0][1]["ang"][1] < 15))
              ):

            return "prone"

        # Side Lying
        elif ((276 < angle_info[1][1]["ang"][1] < 310)
              and (266 < angle_info[0][1]["ang"][1] < 303)
              ):

            return "side lying"
        
        # 4 point kneeling
        elif ((90 < angle_info[1][1]["ang"][0] < 110)
              and ((355 < angle_info[1][1]["ang"][1] < 360) or (0 <= angle_info[1][1]["ang"][1] < 25))
              and (340 < angle_info[0][1]["ang"][0] < 360)
              and ((355 < angle_info[0][1]["ang"][1] < 360) or (0 <= angle_info[0][1]["ang"][1] < 5))
              ):

            return "4 point kneeling"
        
        # Kneeling
        elif ((85 < angle_info[1][1]["ang"][0] < 110)
              and ((345 < angle_info[1][1]["ang"][1] < 360) or (0 <= angle_info[1][1]["ang"][1] < 15))
              and (285 < angle_info[0][1]["ang"][0] < 315)
              and ((355 < angle_info[0][1]["ang"][1] < 360) or (0 <= angle_info[0][1]["ang"][1] < 5))
              ):
            
            return "kneeling"
        
        # Cross Leg Standing
        elif ((0 <= angle_info[1][1]["ang"][0] < 18)
              and (10 < angle_info[1][1]["ang"][1] < 25)
              and (336 < angle_info[0][1]["ang"][0] < 350)
              and (5 < angle_info[0][1]["ang"][1] < 15)
              ):
            
            return "cross leg standing"
        
        # Legs Apart
        elif (((347 < angle_info[1][1]["ang"][0] < 360) or (0 <= angle_info[1][1]["ang"][0] < 8))
              and (340 < angle_info[1][1]["ang"][1] < 354)
              and (345 < angle_info[0][1]["ang"][0] < 360)
              and (334 < angle_info[0][1]["ang"][1] < 345)
              ):
            
            return "legs apart"

        # Knees folded supine
        elif ((325 < angle_info[1][1]["ang"][0] < 340)
              and ((355 < angle_info[1][1]["ang"][1] < 360) or (0 <= angle_info[1][1]["ang"][1] < 5))
              and (200 < angle_info[0][1]["ang"][0] < 210)
              and ((350 < angle_info[0][1]["ang"][1] < 360) or (0 <= angle_info[0][1]["ang"][1] < 5))
              ):
            
            return "knee folded supine"
        
        # Sumo Squat
        elif ((6 < angle_info[1][1]["ang"][0] < 30)
              and (335 < angle_info[1][1]["ang"][1] < 360)
              and (258 < angle_info[0][1]["ang"][0] < 280)
              and (325 < angle_info[0][1]["ang"][1] < 345)):
            
            return "sumo squat"
            
        # Squat 
        elif ((3 < angle_info[1][1]["ang"][0] < 30)
              and ((343 < angle_info[1][1]["ang"][1] < 360) or (0 < angle_info[1][1]["ang"][1] < 3))
              and (277 < angle_info[0][1]["ang"][0] < 302)
              and (335 < angle_info[0][1]["ang"][1] < 360)
              ):
            
            return "squat"

        # Butterfly
        elif ((335 < angle_info[1][1]["ang"][0] < 358)
              and (27 < angle_info[1][1]["ang"][1] < 48)
              and (200 < angle_info[0][1]["ang"][0] < 225)
              and (12 < angle_info[0][1]["ang"][1] < 30)
              ):
            
            return "butterfly"
        
        else:
            return "nopos"

'''  
    def get_ending_and_direction(self, actual_angle_info):
        if len(actual_angle_info) != 3:
            return
        return actual_angle_info

'''

'''       
    def angle_bn_sensor(self, pos_info, angle_info):
        if (len(angle_info) != 2) or (len(pos_info) != 2):
            return
        sensor0_rot = angle_info[0][1]["rot"]
        sensor1_rot = angle_info[1][1]["rot"]
        sensor1_pos = np.array([pos_info[0], pos_info[1], pos_info[2]])
     
    def check_starting_position(self):
        
'''
