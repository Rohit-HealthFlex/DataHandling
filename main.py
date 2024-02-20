import json
import os
import cv2
import matplotlib.pyplot as plt
from tqdm import tqdm

from parser_data import DataParser
from skeleton_model import Skeleton
from visualize import plot_trajectory, plot_fft, get_img_from_fig
from sim_calc import compute_dtw, compute_accumulated_cost_matrix

if __name__ == '__main__':
    folder_name = "data/test/"
    req_cols = "Device name,Acceleration X(g),Acceleration Y(g),Acceleration Z(g),Angle X(°),Angle Y(°),Angle Z(°)"

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

    for exercise_type in os.listdir(folder_name):
        foldername = f"{folder_name}/{exercise_type}/"
        for file in os.listdir(foldername):
            if file.endswith('.csv'):
                filename = f"{foldername}/{file}"
                print(filename)
                obj = DataParser(filename=filename,
                                 req_cols=req_cols)
                device_ids = obj.device_ids
                fig = None
                ax = None
                dev_info = {}
                for device_id in device_ids:
                    head, name = os.path.split(filename)
                    name = f"{os.path.split(head)[-1]}_{name}"
                    target_dir = f"outputs/{name}/{device_id}"
                    pos_info, body_info, acc_info, rot_mat = obj.parse_data(
                        device_id=device_id)
                    dev_info[device_id] = (rot_mat, pos_info)

                for k in tqdm(range(len(rot_mat))):
                    for dev_id in dev_info:
                        T = dev_info[dev_id][0][k]
                        print(k, dev_id)
                        print(T)
                        pos_T = dev_info[dev_id][1][k]

                        sk_obj.update_landmarks(device_id=dev_id,
                                                rot_T=T, trans_T=pos_T)
                        # sk_obj.translate(T=pos_T)

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
        break


# check_based_on_rules()

# fig, ax = plot_trajectory(*pos_info,
#                           *body_info,
#                           fig=fig, ax=ax,
#                           azimuthal_rotation=azimuthal_rotation,
#                           animation=animation, sample_rate=sample_rate,
#                           draw_quiver=draw_quiver,
#                           save=save_trajectory, show=show_trajectory,
#                           target_dir=target_dir, save_video=False)
# plot_fft(*acc_info,
#          save=save_fft, show=show_fft,
#          target_dir=target_dir)
# x = pos_info[0].reshape(-1, 1)
# y = pos_info[1].reshape(-1, 1)
# dist, warp = compute_dtw(x, y)
# print(dist)
# plt.show()
