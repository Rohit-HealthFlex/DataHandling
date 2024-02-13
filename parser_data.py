import os
import pandas as pd
import numpy as np
from scipy.integrate import cumtrapz
import warnings
warnings.filterwarnings("ignore")


class DataParser:
    def __init__(self, filename=None,
                 req_cols=None,
                 animation=True,
                 sample_rate=20):
        self.base_df, self.req_df = self.read_data(
            filename,
            req_cols=req_cols)

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

    def read_data(self, filename, req_cols=None):
        df = pd.read_csv(filename)
        df["Time"], df["Device name"] = df["Device name"], df["Time"]
        if req_cols is None:
            req_cols = df.columns
        if isinstance(req_cols, str):
            req_cols = req_cols.strip().split(",")
        req_df = df[req_cols]
        self.device_ids = req_df["Device name"].unique()
        return df, req_df

    def get_acceleration(self, df):
        acc_x = df["Acceleration X(g)"].to_numpy()
        acc_y = df["Acceleration Y(g)"].to_numpy()
        acc_z = df["Acceleration Z(g)"].to_numpy()
        return acc_x, acc_y, acc_z

    def get_distance(self, acc_x, acc_y, acc_z, dt=0.01):
        x = cumtrapz(cumtrapz(acc_x, dx=dt), dx=dt)
        y = cumtrapz(cumtrapz(acc_y, dx=dt), dx=dt)
        z = cumtrapz(cumtrapz(acc_z, dx=dt), dx=dt)
        return x, y, z

    def get_gyro_angles(self, df):
        pitch = df["Angle X(°)"].to_numpy()
        roll = df["Angle Y(°)"].to_numpy()
        yaw = df["Angle Z(°)"].to_numpy()
        return pitch, roll, yaw

    def parse_data(self, device_id=None, dt=0.01):
        req_df = self.req_df[self.req_df["Device name"] == device_id]
        acc_x, acc_y, acc_z = self.get_acceleration(req_df)
        x, y, z = self.get_distance(acc_x, acc_y, acc_z, dt)
        pitch, roll, yaw = self.get_gyro_angles(req_df)

        earth_x = np.array([[1, 0, 0],]*len(x)).T
        earth_y = np.array([[0, 1, 0],]*len(x)).T
        earth_z = np.array([[0, 0, 1],]*len(x)).T

        # Initialize body Vectors
        body_x = np.empty(earth_x.shape)
        body_y = np.empty(earth_y.shape)
        body_z = np.empty(earth_z.shape)
        rot_xyz = []

        for i in range(x.shape[0]):
            # use negative angles to reverse rotation
            body_x[:, i] = self.R_x(-pitch[i]) @ self.R_y(-roll[i]
                                                          ) @ self.R_z(-yaw[i]) @ earth_x[:, i]
            body_y[:, i] = self.R_x(-pitch[i]) @ self.R_y(-roll[i]
                                                          ) @ self.R_z(-yaw[i]) @ earth_y[:, i]
            body_z[:, i] = self.R_x(-pitch[i]) @ self.R_y(-roll[i]
                                                          ) @ self.R_z(-yaw[i]) @ earth_z[:, i]
            rot_xyz += [self.R_x(-pitch[i]) @ self.R_y(-roll[i]
                                                       ) @ self.R_z(-yaw[i])]
        pos_info = (x, y, z)
        body_info = (body_x, body_y, body_z)
        acc_info = (acc_x, acc_y, acc_z)
        return pos_info, body_info, acc_info, rot_xyz


if __name__ == '__main__':
    folder_name = "data/test/"
    req_cols = "Time,Device name,Acceleration X(g),Acceleration Y(g),Acceleration Z(g),Angle X(°),Angle Y(°),Angle Z(°)"
    device_ids = []

    for exercise_type in os.listdir(folder_name):
        foldername = f"{folder_name}/{exercise_type}/"
        for file in os.listdir(foldername):
            if file.endswith('.csv'):
                filename = f"{foldername}/{file}"
                print(filename)
                obj = DataParser(filename=filename,
                                 req_cols=req_cols)
                device_ids = obj.device_ids
                for device_id in device_ids:
                    head, name = os.path.split(filename)
                    name = f"{os.path.split(head)[-1]}_{name}"
                    target_dir = f"outputs/{name}/{device_id}"
                    pos_info, body_info, acc_info = obj.parse_data(
                        device_id=device_id)
                    # print(pos_info)
