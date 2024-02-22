import json
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from stream_parser import StreamParser
from skeleton_model import Skeleton

# custom stream class
from streamers.data_streamer import Streamer


class StreamAnim:
    def __init__(self):
        self.req_cols = "Device name,Acceleration X(g),Acceleration Y(g),Acceleration Z(g),Angle X(°),Angle Y(°),Angle Z(°)"
        self.data_path = "data/test/Ideal -  Backward Lunge/data__1.csv"
        self.stream_mod = Streamer(filename=self.data_path,
                                   req_cols=self.req_cols)
        self.stream_obj = self.stream_mod.stream()
        self.parser_obj = StreamParser()
        self.map_dict = json.load(open("configs/poser.json"))
        self.map_dict["connections_info"]["24_26"]["device_id"] = "fc:66:87:ee:fb:8c"
        self.map_dict["connections_info"]["26_28"]["device_id"] = "d7:f5:e1:06:da:71"

        self.sk_obj = Skeleton(point_device_map=self.map_dict)
        self.fig = plt.figure(figsize=(8, 8))
        self.ax = self.fig.add_subplot(projection='3d')

        self.use_sensor = "fc:66:87:ee:fb:8c"
        self.sensor_fig = plt.figure(figsize=(8, 8))
        self.sensor_ax = self.sensor_fig.add_subplot()
        self.acc_holder = []
        self.max_size = 100
        self.pointer = 0

    def set_limits(self):
        plt.cla()
        plt.title('Skeleton')

        self.ax.set_xlim((-1, 1))
        self.ax.set_ylim((-1, 1))
        self.ax.set_zlim((-1, 1))

        self.ax.set_xlabel("X")
        self.ax.set_ylabel("Y")
        self.ax.set_zlabel("Z")

    def update(self, i):
        trace = {}
        while len(trace) != len(self.stream_mod.device_ids):
            row = next(self.stream_obj)
            device_id = row["Device name"]
            trace[device_id] = 0
            pos_info, rot_mat = self.parser_obj.stream_parser(row)
            self.sk_obj.update_landmarks(device_id=device_id,
                                         rot_T=rot_mat, trans_T=pos_info)
        self.set_limits()
        pos = np.delete(range(0, len(self.sk_obj.landmarks)),
                        self.sk_obj.skip_points)
        x, y, z = self.sk_obj.landmarks[:,
                                        0], self.sk_obj.landmarks[:, 1],  self.sk_obj.landmarks[:, 2]
        self.ax.scatter(x[pos], y[pos], z[pos])

        for idx in self.sk_obj.joints:
            bone = self.sk_obj.joints[idx]["bone"]
            color, lw = "b", 2
            if self.sk_obj.joints[idx]["device"] != "###":
                color, lw = "r", 4
            st, end = bone[0], bone[1]
            self.ax.plot([x[st], x[end]], [y[st], y[end]],
                         [z[st], z[end]], c=color, lw=lw)
            self.ax.scatter(x[st], y[st], z[st], c=color, lw=lw)
            self.ax.scatter(x[end], y[end], z[end], c=color, lw=lw)

    def draw_sensor_data(self, i):
        row = next(self.stream_obj)
        device_id = row["Device name"]
        if device_id == self.use_sensor:
            plt.cla()
            plt.title(f'acc: {device_id}')
            pos_info, rot_mat = self.parser_obj.stream_parser(row)
            self.acc_holder.append(pos_info)
            np_array = np.array(self.acc_holder)
            print(np_array.shape)
            range_ = list(range(self.pointer, len(
                self.acc_holder)+self.pointer))
            self.sensor_ax.plot(range_, list(np_array[:, 0]), label="X", c="r")
            self.sensor_ax.plot(range_, list(np_array[:, 1]), label="Y", c="g")
            self.sensor_ax.plot(range_, list(np_array[:, 2]), label="Z", c="b")
            plt.legend(loc="upper right")

            self.sensor_ax.set_ylim((-10, 10))

            self.sensor_ax.set_xlabel("Time")
            self.sensor_ax.set_ylabel("acceleration")

            if len(self.acc_holder) > self.max_size:
                self.acc_holder.pop(0)
                self.pointer += 1

    def animate(self):
        self.ani = FuncAnimation(self.sensor_fig,
                                 self.draw_sensor_data,
                                 interval=1)


def main():
    sa = StreamAnim()
    sa.animate()
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()
