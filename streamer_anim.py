import json
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from stream_parser import StreamParser
from skeleton_model import Skeleton

# custom stream class
from streamers.data_streamer import Streamer


class StreamAnim:
    def __init__(self,
                 streamer,
                 map_json,
                 use_sensor=None,
                 skele=True, ms=10):
        self.req_cols = req_cols
        self.stream_mod = streamer
        self.stream_obj = self.stream_mod.stream()
        self.parser_obj = StreamParser()
        self.map_dict = map_json
        self.use_sensor = use_sensor
        self.skele = skele
        self.sk_obj = Skeleton(point_device_map=self.map_dict)

        self.max_size = 25
        self.ms = ms
        self.handles, self.labels = None, None

    def set_limits(self):
        plt.cla()
        plt.title('Skeleton')

        self.sensor_ax.set_xlim((-1, 1))
        self.sensor_ax.set_ylim((-1, 1))
        self.sensor_ax.set_zlim((-1, 1))
        self.sensor_ax.set_xlabel("X")
        self.sensor_ax.set_ylabel("Y")
        self.sensor_ax.set_zlabel("Z")

    def draw_skeleton(self, i):
        trace = {}
        while len(trace) != len(self.stream_mod.device_ids):
            row = next(self.stream_obj)
            device_id = row["Device name"]
            trace[device_id] = 0
            pos_info, rot_mat, _, _ = self.parser_obj.stream_parser(row)
            self.sk_obj.update_landmarks(device_id=device_id,
                                         rot_T=rot_mat, trans_T=pos_info)
        self.set_limits()
        pos = np.delete(range(0, len(self.sk_obj.landmarks)),
                        self.sk_obj.skip_points)
        x, y, z = self.sk_obj.landmarks[:,
                                        0], self.sk_obj.landmarks[:, 1],  self.sk_obj.landmarks[:, 2]
        self.sensor_ax.scatter(x[pos], y[pos], z[pos])

        for idx in self.sk_obj.joints:
            bone = self.sk_obj.joints[idx]["bone"]
            color, lw = "b", 2
            if self.sk_obj.joints[idx]["device"] != "###":
                color, lw = "r", 4
            st, end = bone[0], bone[1]
            self.sensor_ax.plot([x[st], x[end]], [y[st], y[end]],
                                [z[st], z[end]], c=color, lw=lw)
            self.sensor_ax.scatter(x[st], y[st], z[st], c=color, lw=lw)
            self.sensor_ax.scatter(x[end], y[end], z[end], c=color, lw=lw)

    def draw_sensor_data(self, i):
        try:
            row = next(self.stream_obj)
        except:
            return
        device_id = row["Device name"]
        if device_id == self.use_sensor:
            self.sensor_fig.suptitle(f'acc: {device_id}')
            pos_info, _, rot_info, mag_info = self.parser_obj.stream_parser(
                row)
            info = {"acc": pos_info, "rot": rot_info, "mag": mag_info}
            for idx, attr in enumerate(self.holder):
                if self.grid_shape[1] == 2:
                    sensor_ax = self.sensor_ax[idx][0]
                else:
                    sensor_ax = self.sensor_ax[idx]

                if len(self.holder[attr]["value"]) == 0:
                    self.holder[attr]["value"] = info[attr].reshape(1, -1)
                elif len(self.holder[attr]["value"]) > self.max_size:
                    self.holder[attr]["value"] = np.delete(
                        self.holder[attr]["value"], 0, axis=0)
                    self.holder[attr]["pointer"] += 1
                else:
                    self.holder[attr]["value"] = np.concatenate([
                        self.holder[attr]["value"], info[attr].reshape(1, -1)
                    ], axis=0)

                pointer = self.holder[attr]["pointer"]
                np_array = self.holder[attr]["value"]
                range_ = list(range(pointer, len(
                    np_array)+pointer))
                sensor_ax.cla()

                sensor_ax.plot(range_, list(
                    np_array[:, 0]), label="X", c="r")
                sensor_ax.plot(range_, list(
                    np_array[:, 1]), label="Y", c="g")
                sensor_ax.plot(range_, list(
                    np_array[:, 2]), label="Z", c="b")

                sensor_ax.set_ylim(self.holder[attr]["range"])
                sensor_ax.set_xlabel("Time")
                sensor_ax.set_ylabel(self.holder[attr]["name"])

        if self.handles is None and self.labels is None:
            self.handles, self.labels = sensor_ax.get_legend_handles_labels(
            )
            self.sensor_fig.legend(
                self.handles, self.labels, loc='upper right')

    def animate(self):
        if self.skele:
            self.sensor_fig = plt.figure(figsize=(8, 8))
            self.sensor_ax = self.sensor_fig.add_subplot(projection='3d')
            func = self.draw_skeleton
        else:
            self.holder = {"acc": {"value": [], "range": (-10, 10), "name": "acceleration", "pointer": 0},
                           "rot": {"value": [], "range": (0, 360), "name": "rotation", "pointer": 0},
                           "mag": {"value": [], "range": (-180, 180), "name": "magnetometer", "pointer": 0}
                           }
            self.grid_shape = (len(self.holder), 1)
            self.sensor_fig, self.sensor_ax = plt.subplots(
                *self.grid_shape, figsize=(16, 16))
            func = self.draw_sensor_data

        self.ani = FuncAnimation(self.sensor_fig,
                                 func,
                                 interval=self.ms)


def main(params):
    sa = StreamAnim(**params)
    sa.animate()
    plt.show()


if __name__ == "__main__":
    data_path = "data/test/Ideal -  Backward Lunge/data__1.csv"
    req_cols = "Device name,Acceleration X(g),Acceleration Y(g),Acceleration Z(g),Angle X(°),Angle Y(°),Angle Z(°),Magnetic field X(ʯt),Magnetic field Y(ʯt),Magnetic field Z(ʯt)"
    streamer = Streamer(filename=data_path,
                        req_cols=req_cols)
    map_json = json.load(open("configs/poser.json"))
    use_sensor = "fc:66:87:ee:fb:8c"
    map_json["connections_info"]["24_26"]["device_id"] = "fc:66:87:ee:fb:8c"
    map_json["connections_info"]["26_28"]["device_id"] = "d7:f5:e1:06:da:71"

    params = {"streamer": streamer,
              "map_json": map_json,
              "use_sensor": use_sensor,
              "skele": True,
              "ms": 100}

    main(params)
