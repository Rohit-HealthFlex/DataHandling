import json
from src.stream_parser import StreamParser
# custom stream class
from src.rules.presets import Presets
from src.streamers.data_streamer import Streamer
# from src.skeleton_model import Skeleton

from src.rules.rule0 import Rule0
from src.rules.rule0 import Rule_Backward_Lunge

# Not using relative path
data_path = "/home/prathikhf/git_clones/DataHandling/data/test/Custom Sensor Script/data_store_rotatebackwardup.csv"
# Changed column names to fit sensor script
req_cols = "Device name,Acceleration X(g),Acceleration Y(g),Acceleration Z(g),Angle X,Angle Y,Angle Z,Magnetic field X,Magnetic field Y,Magnetic field Z"
streamer = Streamer(filename=data_path,
                    req_cols=req_cols)

preset_obj = Presets()
rule0 = Rule0()
#rule0 = Rule_Backward_Lunge()
parser_obj = StreamParser()
map_json = json.load(open("/home/prathikhf/git_clones/DataHandling/configs/poser.json"))
# pair around which angle has to be calculated
sensor_pairs = [("e5:96:eb:33:1a:dd","e0:3a:df:63:bd:23")] #thigh first, then shin

devices_pos_dict = {}
for row in streamer.stream():
    device_id = row["Device name"]

    # preprocessing
    pos_info, acc_info, rot_xyz, rot_info, mag_info, rot_mat = parser_obj.stream_parser(
        row)
    devices_pos_dict[device_id] = {"pos": pos_info,
                                   "rot": rot_mat}
    angle_info = []
    for sensors in sensor_pairs:
        sensor0, sensor1 = sensors
        if sensor0 in devices_pos_dict and sensor1 in devices_pos_dict:
            angle_info.append((sensor0, devices_pos_dict[sensor0]))
            angle_info.append((sensor1, devices_pos_dict[sensor1]))
        else:
            angle_info = []

    # getting required computations
    direction = preset_obj.get_direction(rot_info)
    position = preset_obj.get_position(pos_info)
    angle_info = preset_obj.get_angle(angle_info)
    dist_info = preset_obj.get_distance(pos_info)

    # applying rules
    rule_flag, error_info = rule0.apply_rule(
        direction, position, angle_info, dist_info)
    print(rule_flag, error_info, "\n\n")
