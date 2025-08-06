import json
import os
import re

base_path = r"Z:\zju-mocap\CoreView_313-008\CoreView_313"
input_transforms_path = os.path.join(base_path, "transforms.json")

output_train_path = os.path.join(base_path, "transforms_train.json")
output_val_path = os.path.join(base_path, "transforms_val.json")
output_test_path = os.path.join(base_path, "transforms_test.json")

# Define camera IDs for val and test
val_test_camera_ids = [2, 7, 10, 21]
val_camera_ids = [2, 7]
test_camera_ids = [10, 21]

def load_transforms(path):
    with open(path, 'r') as f:
        return json.load(f)

def save_transforms(data, path):
    with open(path, 'w') as f:
        json.dump(data, f, indent=4)

def extract_camera_id(file_path):
    match = re.search(r'cam(\d+)', file_path)
    return int(match.group(1)) if match else None

def main():
    data = load_transforms(input_transforms_path)
    frames = data['frames']
    camera_angle_x = data.get('camera_angle_x', 0.691)

    train_frames = []
    val_frames = []
    test_frames = []

    for frame in frames:
        cam_id = extract_camera_id(frame['file_path'])

        if cam_id in val_camera_ids:
            val_frames.append(frame)
        elif cam_id in test_camera_ids:
            test_frames.append(frame)
        else:
            train_frames.append(frame)

    train_data = {
        "camera_angle_x": camera_angle_x,
        "frames": train_frames
    }
    val_data = {
        "camera_angle_x": camera_angle_x,
        "frames": val_frames
    }
    test_data = {
        "camera_angle_x": camera_angle_x,
        "frames": test_frames
    }

    save_transforms(train_data, output_train_path)
    save_transforms(val_data, output_val_path)
    save_transforms(test_data, output_test_path)

    print(f"Saved train transforms: {output_train_path} ({len(train_frames)} frames)")
    print(f"Saved val transforms: {output_val_path} ({len(val_frames)} frames)")
    print(f"Saved test transforms: {output_test_path} ({len(test_frames)} frames)")

if __name__ == "__main__":
    main()
