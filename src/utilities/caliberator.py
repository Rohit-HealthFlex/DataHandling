import numpy as np


class Caliberate:
    def __init__(self, id):
        self.id = id
        # 0 : x, 1: y, 2: z
        self.default_axis = {'front': 0, 'side': 1, 'up': 2}
        self.default_dir = {'front': 1, 'side': 1, 'up': 1}
        self.pos_list = []
        self.calib_axis = {'front': None, 'side': None, 'up': None}
        self.calib_dir = {'front': None, 'side': None, 'up': None}
        self.duration = 50

    def get_dominant_axis(self, vector):
        return np.argmax(np.abs(vector))

    def get_caliberation(self, mode):

        start = self.pos_list[0]
        end = self.pos_list[-1]
        diff = end - start

        axis = self.get_dominant_axis(diff)
        direction = diff[axis]/abs(diff[axis])

        self.calib_axis[mode] = axis
        self.calib_dir[mode] = int(direction)
        return axis, int(direction)

    def caliberate(self, pos_info, mode='front'):
        if len(self.pos_list) < self.duration:
            self.pos_list.append(pos_info)
            return None, None

        axis, direction = self.get_caliberation(mode)
        self.pos_list = []
        return axis, direction

    def auto_calibration(self, axis_info_vector):
        print("axes : ", self.calib_axis)
        print("dir : ", self.calib_dir)
        permute_axis = list(self.calib_axis.values())
        dir_values = np.array(list(self.calib_dir.values()))
        axis_info_vector[[0, 1, 2]] = axis_info_vector[permute_axis]
        axis_info_vector *= dir_values
        return axis_info_vector


if __name__ == '__main__':
    obj = Caliberate('123')

    def_axis = ["front", "side", "up"]

    expected_axis = ["up", "side", "front"]
    movement_axis = ["front", "up", "side"]
    dir_ = [-1, 1, 1]

    for ax, mv_ax, d in zip(expected_axis, movement_axis, dir_):
        print(f"Exp move : {ax}/{def_axis.index(ax)}")
        print(f"Obs move : {mv_ax}/{def_axis.index(mv_ax)}")
        print(f"dir : {d}")
        for i in range(100):
            vec = np.random.random((3,))
            # up
            mv_ax_ = def_axis.index(mv_ax)
            vec[mv_ax_] += (d*i)
            axis, direction = obj.caliberate(vec, ax)
            if axis is not None:
                break
        print(axis, direction)
        print("-----------------")

    base_vec = np.array([1.55, 2.97, 3.001]).reshape((3,))
    perm_base_vec = obj.auto_calibration(base_vec.copy())
    print(base_vec, "->", perm_base_vec)
