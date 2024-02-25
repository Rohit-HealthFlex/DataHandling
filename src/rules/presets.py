from src.utilities.utils import calculate_rot_angle


class Presets:
    def __init__(self):
        self.direction = {"z": ["top", "down", ""],
                          "y": ["left", "right", ""],
                          "x": ["front", "back", ""]}

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
        if len(angle_info) != 2:
            return
        sensor0_rot = angle_info[0][1]["rot"]
        sensor1_rot = angle_info[1][1]["rot"]
        out = calculate_rot_angle(sensor0_rot, sensor1_rot)
        return out

    def get_position(self, pos_info):
        if len(pos_info) != 3:
            return
        return {"x": pos_info[0],
                "y": pos_info[1],
                "z": pos_info[2]}
