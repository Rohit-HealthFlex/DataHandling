import os
import json
import cv2
import pandas as pd
import matplotlib.pyplot as plt

from stream_parser import StreamParser
from skeleton_model import Skeleton
from visualize import plot_trajectory, plot_fft, get_img_from_fig
from sim_calc import compute_dtw, compute_accumulated_cost_matrix

# custom stream class


class Streamer:
    def __init__(self, filename, req_cols=None):
        self.df, self.req_df = self.read_data(filename,
                                              req_cols=req_cols)

    def read_data(self, filename, req_cols=None):
        df = pd.read_csv(filename)
        df = df.reset_index()
        df.iloc[:, :] = df.iloc[:, :].shift(axis=1)
        df = df.drop(["index"], axis=1)
        if isinstance(req_cols, str):
            req_cols = req_cols.strip().split(",")
        req_df = df[req_cols]
        self.device_ids = req_df["Device name"].unique()
        return df, req_df

    def stream(self):
        for i in range(len(self.req_df)):
            yield self.req_df.iloc[i, :]


if __name__ == "__main__":
    req_cols = "Device name,Acceleration X(g),Acceleration Y(g),Acceleration Z(g),Angle X(°),Angle Y(°),Angle Z(°)"
    data_path = "data/test/Ideal -  Backward Lunge/data__1.csv"
    stream_obj = Streamer(filename=data_path,
                          req_cols=req_cols)

    device_ids = []
    animation = True
    sample_rate = 30
    draw_quiver = True
    save_trajectory = False
    show_trajectory = True
    save_fft = False
    show_fft = True
    azimuthal_rotation = 10
    save_video = False

    parser_obj = StreamParser()

    map_dict = json.load(open("configs/poser.json"))
    # perform mapping segment -> imu sensor
    map_dict["connections_info"]["24_26"]["device_id"] = "fc:66:87:ee:fb:8c"
    map_dict["connections_info"]["26_28"]["device_id"] = "d7:f5:e1:06:da:71"

    sk_obj = Skeleton(point_device_map=map_dict)
    base_fig = sk_obj.plot_skeleton(save_video=save_video)
    target_dir = "test"
    os.makedirs(target_dir, exist_ok=True)
    name = "skeleton_video-37-155_simultaneous.mp4"
    video_fr = 5
    if save_video:
        base_fr = get_img_from_fig(base_fig)
        height, width, _ = base_fr.shape
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        video = cv2.VideoWriter(
            f'{target_dir}/{name.split(".")[0]}.mp4',
            fourcc, video_fr,
            (width, height))

    for idx, row in enumerate(stream_obj.stream()):
        device_id = row["Device name"]
        pos_info, rot_mat = parser_obj.stream_parser(row)

        print(idx, device_id)
        print(rot_mat)
        sk_obj.update_landmarks(device_id=device_id,
                                rot_T=rot_mat, trans_T=pos_info)
        # sk_obj.translate(T=pos_info)
        fig = sk_obj.plot_skeleton(save_video=save_video)
        if save_video:
            frame = get_img_from_fig(fig)
            video.write(frame)
        else:
            plt.pause(0.1)
    if save_video:
        cv2.destroyAllWindows()
        video.release()
    else:
        plt.show()
