import numpy as np


def get_angle(x, y):
    x = x/np.linalg.norm(x)
    y = y/np.linalg.norm(y)
    dot_product = np.dot(x, y)
    angle = np.arccos(dot_product)
    return np.rad2deg(angle)


def get_angle_bw_line_segments(line1: tuple, line2: tuple):
    p0_p1 = line1[0] - line1[1]
    p1_p2 = line2[0] - line2[1]
    angle = abs(get_angle(p0_p1, p1_p2))
    return angle if angle <= 90 else angle - 90


p0 = [0, 1, 3]
p1 = [0, 0, 4]
p2 = [2, 1, 1]
line1 = (np.array(p0), np.array(p1))
line2 = (np.array(p1), np.array(p2))
angle = get_angle_bw_line_segments(line1, line2)
print(angle)
