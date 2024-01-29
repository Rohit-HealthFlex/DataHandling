import os
import matplotlib.pyplot as plt

from parser_data import DataParser
from visualize import plot_trajectory, plot_fft
from sim_calc import compute_dtw, compute_accumulated_cost_matrix

if __name__ == '__main__':
    folder_name = "data/test/"
    req_cols = "Device name,Acceleration X(g),Acceleration Y(g),Acceleration Z(g),Angle X(°),Angle Y(°),Angle Z(°)"
    device_ids = []
    animation = False
    sample_rate = 30
    draw_quiver = True
    save_trajectory = False
    show_trajectory = True
    save_fft = True
    show_fft = True
    azimuthal_rotation = 10

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
                for device_id in device_ids:
                    head, name = os.path.split(filename)
                    name = f"{os.path.split(head)[-1]}_{name}"
                    target_dir = f"outputs/{name}/{device_id}"
                    pos_info, body_info, acc_info = obj.parse_data(
                        device_id=device_id)
                    # check_based_on_rules()
                    fig, ax = plot_trajectory(*pos_info,
                                              *body_info,
                                              fig=fig, ax=ax,
                                              azimuthal_rotation=azimuthal_rotation,
                                              animation=animation, sample_rate=sample_rate,
                                              draw_quiver=draw_quiver,
                                              save=save_trajectory, show=show_trajectory,
                                              target_dir=target_dir, save_video=False)
                plot_fft(*acc_info,
                         save=save_fft, show=show_fft,
                         target_dir=target_dir)
                # x = pos_info[0].reshape(-1, 1)
                # y = pos_info[1].reshape(-1, 1)
                # dist, warp = compute_dtw(x, y)
                # print(dist)
                plt.show()

        # break
