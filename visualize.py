import io
import cv2
import os
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

import warnings
warnings.filterwarnings("ignore")


def get_img_from_fig(fig, dpi=180):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=dpi)
    buf.seek(0)
    img_arr = np.frombuffer(buf.getvalue(), dtype=np.uint8)
    buf.close()
    img = cv2.imdecode(img_arr, 1)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    return img


def plot_trajectory(
        x, y, z,
        body_x, body_y, body_z,
        fig=None, ax=None,
        azimuthal_rotation=10,
        animation=True, sample_rate=20,
        draw_quiver=True, save=True, show=True,
        save_video=True, video_fr=5,
        target_dir="outputs",
        name="trajectory.png"):

    print("Working on..", target_dir)
    distance = np.sqrt(x[-1]**2 + y[-1]**2 + z[-1]**2)
    quiver_len = 0.5  # 0.01 * distance
    if fig is None:
        fig, ax = plt.subplots()
        fig.suptitle(f"{target_dir}-trajectory&angle", fontsize=20)
        ax = plt.axes(projection='3d')

    width, height = 1152, 864
    if save_video:
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        video = cv2.VideoWriter(
            f'{target_dir}/{name.split(".")[0]}.mp4',
            fourcc, video_fr,
            (width, height))

    for i in tqdm(range(0, len(x), sample_rate)):
        ax.scatter3D(x[i], y[i], z[i], 'k', lw=1.5,
                     label='trajectory', color="r")
        ax.plot3D(x, y, z, 'k', lw=1, label='trajectory', color="b")
        if draw_quiver:
            # plot x vectors
            ax.quiver(x[i], y[i], z[i],
                      body_x[0][i], body_x[1][i], body_x[2][i],
                      color='b', label='x axis', length=quiver_len)
            # Plot y vectors
            ax.quiver(x[i], y[i], z[i],
                      body_y[0][i], body_y[1][i], body_y[2][i],
                      color='r', label='y axis', length=quiver_len)
            # Plot Z vectors
            ax.quiver(x[i], y[i], z[i],
                      body_z[0][i], body_z[1][i], body_z[2][i],
                      color='g', label='z axis', length=quiver_len)
        if animation:
            plt.pause(.01)
        if save_video:
            fig_image = get_img_from_fig(fig)
            video.write(fig_image)

        ax.azim += azimuthal_rotation

    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")

    if save:
        os.makedirs(target_dir, exist_ok=True)
        plt.savefig(os.path.join(target_dir, name))
    # if show:
    #     plt.show()

    if save_video:
        cv2.destroyAllWindows()
        video.release()
    return fig, ax


def plot_fft(acc_x, acc_y, acc_z, dt=0.01,
             save=True, show=True,
             target_dir="outputs",
             name="fft_noise.png"):
    freq = np.fft.rfftfreq(acc_x.shape[0], d=dt)
    fft_x = np.fft.rfft(acc_x)
    fft_y = np.fft.rfft(acc_y)
    fft_z = np.fft.rfft(acc_z)
    fig4, [ax1, ax2, ax3] = plt.subplots(3, 1, sharex=True, sharey=True)
    fig4.suptitle(f'{target_dir}-Noise Spectrum', fontsize=20)
    ax1.plot(freq, abs(fft_x), c='r', label='x noise')
    ax1.legend()
    ax2.plot(freq, abs(fft_y), c='b', label='y noise')
    ax2.legend()
    ax3.plot(freq, abs(fft_z), c='g', label='z noise')
    ax3.legend()
    ax3.set_xlabel('Freqeuncy (Hz)')

    if save:
        os.makedirs(target_dir, exist_ok=True)
        plt.savefig(os.path.join(target_dir, name))
    if show:
        plt.show()
