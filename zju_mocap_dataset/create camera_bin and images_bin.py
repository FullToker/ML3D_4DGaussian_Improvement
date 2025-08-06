import json
import os
import struct
import numpy as np
from scipy.spatial.transform import Rotation as R


def write_cameras_bin(K_list, output_path, width=1024, height=1024):
    print(f"Writing {len(K_list)} cameras to {output_path}")
    with open(output_path, 'wb') as f:
        f.write(struct.pack('<Q', len(K_list)))

        for cam_id, K in enumerate(K_list):
            model_id = 1
            fx = K[0][0]
            fy = K[1][1]
            cx = K[0][2]
            cy = K[1][2]
            params = [fx, fy, cx, cy]

            cam_id_out = cam_id + 1

            print(f"  Camera {cam_id_out}: fx={fx:.2f}, fy={fy:.2f}, cx={cx:.2f}, cy={cy:.2f}")

            f.write(struct.pack('<IIQQ', cam_id_out, model_id, width, height))
            f.write(struct.pack('<' + 'd' * len(params), *params))

    print("Finished cameras.bin")


import struct
import os
import numpy as np
from scipy.spatial.transform import Rotation as R


def write_images_bin_subset(R_list, T_list, output_path, camera_folder_base, images_per_cam=10):
    """
    Writes COLMAP images.bin file with no 2D points (empty tracks),
    expecting cam00, cam01... with images named frame_00001.jpg, ...
    """
    with open(output_path, 'wb') as f:
        total_images = len(R_list) * images_per_cam
        f.write(struct.pack('<Q', total_images))

        image_id = 1
        for cam_id, (R_mat, T_vec) in enumerate(zip(R_list, T_list)):
            q = R.from_matrix(R_mat).as_quat()
            qvec = [q[3], q[0], q[1], q[2]]
            tvec = np.array(T_vec).flatten()

            camera_id = cam_id + 1

            for i in range(images_per_cam):
                f.write(struct.pack('<i', image_id))
                f.write(struct.pack('<4d', *qvec))
                f.write(struct.pack('<3d', *tvec))
                f.write(struct.pack('<i', camera_id))

                # 👇 Updated image path
                path = f"cam{cam_id + 1:02d}/frame_{i + 1:05d}.jpg"
                f.write(path.encode('utf-8') + b'\x00')

                # No 2D points
                f.write(struct.pack('<Q', 0))

                image_id += 1

    print(f"Wrote {total_images} images to {output_path}")

    from collections import defaultdict
    stats = defaultdict(int)
    with open(output_path, 'rb') as f:
        stats['total_images'] = struct.unpack('<i', f.read(4))[0]
        for _ in range(stats['total_images']):
            stats['fixed_block'] += len(f.read(64))
            while f.read(1) != b'\x00': stats['path_len'] += 1
            stats['footer'] += len(f.read(8))

    print(f"\nValidation:")
    print(f"Total images: {stats['total_images']}")
    print(f"Fixed blocks: {stats['fixed_block']} bytes")
    print(f"Paths: {stats['path_len']} chars")
    print(f"Footers: {stats['footer']} bytes")
    print(f"File size: {os.path.getsize(output_path)} bytes")



def main():
    print("Loading camera data...")
    with open(r"Z:\zju-mocap\CoreView_313-008\CoreView_313\K, R, T, D cams_only.json", "r") as f:
        data = json.load(f)

    cams = data["cams"]["20190823"]
    K_list = cams["K"]
    R_list = cams["R"]
    T_list = cams["T"]

    assert len(K_list) == len(R_list) == len(T_list), "Mismatch in number of cameras"

    output_dir = r"Z:\zju-mocap\CoreView_313-008\CoreView_313"
    os.makedirs(output_dir, exist_ok=True)

    write_cameras_bin(K_list, os.path.join(output_dir, "cameras.bin"))
    write_images_bin_subset(R_list, T_list, os.path.join(output_dir, "images.bin"), camera_folder_base=output_dir, images_per_cam=10)

    print("Finished writing cameras.bin and images.bin")


if __name__ == "__main__":
    main()
