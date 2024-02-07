import os
import cv2
import json
import mediapipe as mp
import numpy as np
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose


def postprocess_json(pose_data):
    landmark = pose_data["landmarks"]
    joints = pose_data["connections"]

    final_out = {}
    final_out["landmarks"] = {}
    for l in landmark:
        points = landmark[l]
        points[-1] = 0
        final_out["landmarks"][l] = points

    vec = []
    for j in joints:
        dict_ = {}
        dict_["point_pairs"] = j
        dict_["device_id"] = "###"
        dict_["centricity"] = 0.5
        vec.append(dict_)

    # vec[3]["device_id"] = "123"
    # final_out["connections_info"] = vec

    return final_out


def initialize_skeleton(image_files,
                        target_folder="configs"):
    out_dict = {}
    BG_COLOR = (192, 192, 192)  # gray
    with mp_pose.Pose(
            static_image_mode=True,
            model_complexity=2,
            enable_segmentation=True,
            min_detection_confidence=0.5) as pose:
        for idx, file in enumerate(image_files):
            image = cv2.imread(file)
            image_height, image_width, _ = image.shape
            results = pose.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

            if not results.pose_landmarks:
                continue
            print(
                f'Nose coordinates: ('
                f'{results.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE].x * image_width}, '
                f'{results.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE].y * image_height})'
            )

            annotated_image = image.copy()
            condition = np.stack(
                (results.segmentation_mask,) * 3, axis=-1) > 0.1
            bg_image = np.zeros(image.shape, dtype=np.uint8)
            bg_image[:] = BG_COLOR
            annotated_image = np.where(condition, annotated_image, bg_image)
            mp_drawing.draw_landmarks(
                annotated_image,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())

            print(list(mp_pose.POSE_CONNECTIONS))

            landmark_dict = {}
            for idx, val in enumerate(results.pose_world_landmarks.landmark):
                landmark_dict[idx] = (val.x, val.y, 0)

            out_dict["landmarks"] = landmark_dict
            out_dict["connections"] = list(mp_pose.POSE_CONNECTIONS)
            # Plot pose world landmarks.
            mp_drawing.plot_landmarks(
                results.pose_world_landmarks, mp_pose.POSE_CONNECTIONS)

            out_dict = postprocess_json(out_dict)
            save_path = os.path.join(target_folder, file.split(".")[0]+".json")
            with open(save_path, "w") as f:
                json.dump(out_dict, f, indent=4)


if __name__ == "__main__":
    image_files = ["person.png"]
    initialize_skeleton(image_files)
