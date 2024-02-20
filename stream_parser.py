import os
import pandas as pd
import numpy as np
from scipy.integrate import cumtrapz
import warnings
warnings.filterwarnings("ignore")


class StreamParser:
    def __init__(self):
        pass

    @staticmethod
    def R_x(x):
        # body frame rotation about x axis
        x = np.deg2rad(x)
        return np.array([[1,      0,       0],
                        [0, np.cos(-x), -np.sin(-x)],
                        [0, np.sin(-x), np.cos(-x)]])

    @staticmethod
    def R_y(y):
        # body frame rotation about y axis
        y = np.deg2rad(y)
        return np.array([[np.cos(-y), 0, -np.sin(-y)],
                        [0,      1,        0],
                        [np.sin(-y), 0, np.cos(-y)]])

    @staticmethod
    def R_z(z):
        # body frame rotation about z axis
        z = np.deg2rad(z)
        return np.array([[np.cos(-z), -np.sin(-z), 0],
                        [np.sin(-z), np.cos(-z), 0],
                        [0,      0,       1]])

    def get_linear_acceleration(self, df):
        acc_x = df["Acceleration X(g)"]
        acc_y = df["Acceleration Y(g)"]
        acc_z = df["Acceleration Z(g)"]
        return acc_x, acc_y, acc_z

    def get_distance(self, acc_x, acc_y, acc_z, dt=0.01):
        x = cumtrapz(cumtrapz(acc_x, dx=dt), dx=dt)
        y = cumtrapz(cumtrapz(acc_y, dx=dt), dx=dt)
        z = cumtrapz(cumtrapz(acc_z, dx=dt), dx=dt)
        return x, y, z

    def get_gyro_angles(self, df):
        pitch = df["Angle X(°)"]+180
        roll = df["Angle Y(°)"]+180
        yaw = df["Angle Z(°)"]+180
        return pitch, roll, yaw

    def stream_parser(self, row, dt=0.01):
        pitch, roll, yaw = self.get_gyro_angles(row)
        lin_x, lin_y, lin_z = self.get_linear_acceleration(row)

        earth_x = np.array([1, 0, 0]).T
        earth_y = np.array([0, 1, 0]).T
        earth_z = np.array([0, 0, 1]).T

        rot_x, rot_y, rot_z = self.R_x(-pitch), self.R_y(-roll), self.R_z(-yaw)
        rot_xyz = rot_x @ rot_y @ rot_z
        lin_acc_vec = np.array([lin_x, lin_y, lin_z])

        acc_x_earth, acc_y_earth, acc_z_earth = np.dot(rot_xyz, lin_acc_vec)

        # trans = np.array([x_earth, y_earth, z_earth])
        # rot_xyz[:, -1] += trans

        # x, y, z = self.get_distance(x, y, z, dt=dt)
        pos_info = np.array([acc_x_earth, acc_y_earth, acc_z_earth]).T
        return pos_info, rot_xyz
