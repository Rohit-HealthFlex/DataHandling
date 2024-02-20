import matplotlib.pyplot as plt
import numpy as np


def show_lines_angles(out_dict):
    for k in out_dict:
        seg1 = out_dict[k]["seg1"]
        seg2 = out_dict[k]["seg2"]
        angle = out_dict[k]["angle"]

        plt.plot([seg1[0][0], seg1[1][0]],
                 [seg1[0][1], seg1[1][1]])
        plt.plot([seg2[0][0], seg2[1][0]],
                 [seg2[0][1], seg2[1][1]])
        plt.title(f"{k} : angle: {angle}")
        plt.show()


def get_angle(x, y):
    if x.any():
        x = x/np.linalg.norm(x)
    if y.any():
        y = y/np.linalg.norm(y)
    dot_product = np.dot(x, y)
    angle = np.arccos(dot_product)
    return np.rad2deg(angle)


def get_angle_bw_line_segments(line1, line2):
    p0_p1 = line1[1] - line1[0]
    p1_p2 = line2[0] - line2[1]
    angle = abs(get_angle(p0_p1, p1_p2))
    return angle  # if angle <= 90 else angle - 90


def get_axis_wise_angles(line1, line2):
    pairs = {"x-y": [0, 1], "y-z": [1, 2], "x-z": [0, 2]}
    out = {}
    for k, pair in pairs.items():
        seg1 = (line1[0][pair], line1[1][pair])
        seg2 = (line2[0][pair], line2[1][pair])
        angle = get_angle_bw_line_segments(seg1, seg2)
        out[k] = {"seg1": seg1, "seg2": seg2, "angle": angle}
    return out


# p0 = [0, 0, 0]
# p1 = [1, 1, 0]
# p2 = [2, -1, 1]
# line1 = (np.array(p0), np.array(p1))
# line2 = (np.array(p1), np.array(p2))
# angle = get_angle_bw_line_segments(line1, line2)
# print(angle)

# out = get_axis_wise_angles(line1, line2)
# for k in out:
#     print(k, "->", out[k]["angle"])
# show_lines_angles(out)
