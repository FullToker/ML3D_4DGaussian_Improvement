import json
import os
import re

# Paths
base_path = r"Z:\zju-mocap\CoreView_313-008\CoreView_313"
times_path = os.path.join(base_path, "image_times.json")
transform_path = r"C:\Users\Tom1\Desktop\transform.txt"
output_path = os.path.join(base_path, "transforms.json")

# Load JSON
def load_json(path):
    with open(path, 'r') as f:
        return json.load(f)

def cam_key_to_index(cam_key):
    match = re.match(r'cam(\d+)', cam_key)
    if match:
        return int(match.group(1))
    return -1

def main():
    camera_data = load_json(transform_path)
    image_times = load_json(times_path)
    print("Loaded cameras:", sorted(camera_data.keys()))
    num_frames_per_camera = 15
    camera_angle_x_default = 0.691
    frames = []

    for cam_key, cam_info in camera_data.items():
        cam_index = cam_key_to_index(cam_key)
        if cam_index == -1:
            continue

        for frame_idx in range(num_frames_per_camera):
            file_path = f"./cam{cam_index:02d}/frame_{frame_idx + 1:05d}"

            frame = {
                "file_path": file_path,
                "rotation": cam_info.get("rotation", 0.0),
                "time": cam_info.get("time", 0.0),
                "transform_matrix": cam_info.get("transform_matrix", [[1, 0, 0, 0],
                                                                      [0, 1, 0, 0],
                                                                      [0, 0, 1, 0],
                                                                      [0, 0, 0, 1]])
            }

            try:
                frame["time"] = image_times[frame_idx]["time_sec"]
            except (IndexError, KeyError, TypeError):
                pass

            frames.append(frame)

    transforms_data = {
        "camera_angle_x": camera_angle_x_default,
        "frames": frames
    }

    with open(output_path, 'w') as f:
        json.dump(transforms_data, f, indent=4)

    print(f"Saved combined transforms file to {output_path}")

if __name__ == "__main__":
    main()
