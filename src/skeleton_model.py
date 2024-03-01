import json
import cv2
from copy import deepcopy
import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial.transform import Rotation as R

from src.utilities.utils import get_angle_bw_line_segments


def normalize(st, end, expected_length=0.3):
    dir_vector = end - st
    norm_dir = np.linalg.norm(dir_vector)

    scale = norm_dir / expected_length[0]
    if 0.5 > scale or scale > 1.5:
        # print("#####", scale, norm_dir, expected_length[0])
        end = dir_vector/scale
        # print("###after change", np.linalg.norm(end))
        # else:
        #     scale = norm_dir / expected_length[0]
        #     end = dir_vector/scale
    # for i in range(0, len(dir_vector)):
    #     dir_vector[i] = max(dir_vector[i], dir_vector[i]+expected_length[i+1])
    return st, end


def rotation_matrix_2d(axis, theta):
    c, s = np.cos(theta), np.sin(theta)
    rot_mat = np.matrix([[c, -s, 0],
                        [s, c, 0],
                        [0, 0, 1]])

    return rot_mat


def rotation_matrix_3d(axis, theta):
    r = R.from_rotvec([
        [0, 0, theta],
        [theta, 0, 0],
        [0, theta, 0]])
    return r.as_rotvec()


class Segment:
    def __init__(self, pos, device_id="###", device_centricity=0.5):
        self.pos = pos
        self.device_id = device_id
        self.device_centricity = device_centricity

    def rotate_joint(self, vec, rot_mat):
        out = np.dot(rot_mat, vec)
        return out

    def update_segment(self, landmarks, T):
        rot_T, trans_T = T
        p0, p1 = self.pos
        vec0, vec1 = landmarks[p0], landmarks[p1]

        vec0 = self.rotate_joint(vec0, rot_T)
        vec1 = self.rotate_joint(vec1, rot_T)
        # print("after rotation", self.device_id, vec0)

        # # maybe reset
        # vec0 += trans_T
        # vec1 += trans_T

        # print("after translation", self.device_id, vec0)
        # vec0, vec1 = self.normalize(vec0, vec1)
        landmarks[p0] = vec0
        landmarks[p1] = vec1
        return landmarks


class Skeleton:

    def __init__(self, point_device_map,
                 skip_points=[17, 19, 21, 22, 20, 18, 31, 29,
                              30, 32, 7, 3, 2, 1, 0, 4, 5, 6, 8, 9, 10]):
        self.landmarks = np.array(list(point_device_map["landmarks"].values()))
        self.skip_points = skip_points
        self.joints = {}
        self.point_device_map = {}
        for idx, key in enumerate(point_device_map["connections_info"]):
            values = point_device_map["connections_info"][key]
            point_pair = values["point_pairs"]
            if int(point_pair[0]) in skip_points or int(point_pair[1]) in skip_points:
                continue
            device_id = values["device_id"]
            device_centricity = values["centricity"]
            if device_id != "###":
                self.point_device_map[device_id] = Segment(
                    point_pair, device_id, device_centricity)
            self.joints[idx] = {"bone": point_pair, "device": device_id}
        self.mean_length = self.get_mean_length()
        self.init_landmark = deepcopy(self.landmarks)
        self.azim = 90
        self.elev = 90
        # self.trajectory = [base_landmarks]

    def get_mean_length(self):
        mean_length = {}
        for idx in self.joints:
            bone = self.joints[idx]["bone"]
            st, end = bone[0], bone[1]
            vec0, vec1 = self.landmarks[st], self.landmarks[end]
            norm_diff = np.linalg.norm(vec0-vec1)
            diff = list(vec0 - vec1)
            mean_length[f"{st}_{end}"] = [norm_diff, *diff]
        return mean_length

    def update_landmarks(self, device_id, rot_T, trans_T):
        segment = self.point_device_map[device_id]
        T = [rot_T, trans_T]
        self.landmarks = segment.update_segment(self.landmarks, T)

    def translate(self, T):
        self.landmarks += T

    def estimate_angle(self):
        for dev_id in self.point_device_map:
            point_pair = self.point_device_map[dev_id].pos
            for rem_idx in self.joints:
                rem_points = self.joints[rem_idx]["bone"]
                if point_pair[0] in rem_points or point_pair[1] in rem_points:
                    line1 = self.landmarks[point_pair]
                    line2 = self.landmarks[rem_points]
                    angle = get_angle_bw_line_segments(line1, line2)


if __name__ == "__main__":
    dev_id = "fc:66:87:ee:fb:8c"
    map_dict = json.load(open("configs/poser.json"))
    map_dict["connections_info"]["26_28"]["device_id"] = dev_id
    sk_obj = Skeleton(point_device_map=map_dict)
    sk_obj.plot_skeleton()

    for idx in range(10):
        print(idx)
        axis = [4, 4, 1]
        theta = np.pi/np.random.uniform(1, 4)
        T = rotation_matrix_3d(axis, theta).reshape(1, 3, 3)
        print(T.shape)
        sk_obj.update_landmarks(dev_id, T)
        # sk_obj.estimate_angle()
        sk_obj.plot_skeleton()

        # plt.pause(1)
        # plt.close()
        print("--------")
    # plt.show()