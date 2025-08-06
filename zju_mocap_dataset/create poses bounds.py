
import json
import numpy as np


def load_data(json_path):
    with open(json_path, 'r') as f:
        data = json.load(f)
    cams = data["cams"]["20190823"]
    K_list = cams["K"]
    R_list = cams["R"]
    T_list = cams["T"]

    assert len(K_list) == len(R_list) == len(T_list), \
        f"Length mismatch: K={len(K_list)}, R={len(R_list)}, T={len(T_list)}"

    print(f"Loaded {len(K_list)} cameras from JSON.")
    return K_list, R_list, T_list

def compute_pose_bounds(K_list, R_list, T_list, near=0.1, far=4.0):
    poses_bounds = []

    for i, (K, R_mat, T) in enumerate(zip(K_list, R_list, T_list)):
        K = np.array(K)
        R_mat = np.array(R_mat)
        T = np.array(T).reshape(3)

        assert K.shape == (3, 3), f"Camera {i} K shape invalid: {K.shape}"
        assert R_mat.shape == (3, 3), f"Camera {i} R shape invalid: {R_mat.shape}"
        assert T.shape == (3,), f"Camera {i} T shape invalid: {T.shape}"

        c2w = np.eye(4)
        c2w[:3, :3] = R_mat.T
        c2w[:3, 3] = -R_mat.T @ T

        c2w[:3, 1:3] *= -1

        pose_padded = np.pad(c2w[:3, :], ((0, 0), (0, 1)), constant_values=0)

        bounds_padded = np.pad(np.array([[near, far, 0, 0]]), ((0, 1), (0, 1)), constant_values=0)

        pose_bounds = np.vstack([pose_padded, bounds_padded])

        assert pose_bounds.shape == (5, 5), f"Camera {i} pose_bounds shape invalid: {pose_bounds.shape}"

        poses_bounds.append(pose_bounds)

    poses_bounds = np.stack(poses_bounds, axis=0)
    print(f"Generated poses_bounds array of shape: {poses_bounds.shape}")
    return poses_bounds


def main():
    json_path = r"Z:\zju-mocap\CoreView_313-008\CoreView_313\K, R, T, D cams_only.json"
    output_path = r"Z:\zju-mocap\CoreView_313-008\CoreView_313\poses_bounds_multipleview.npy"

    K_list, R_list, T_list = load_data(json_path)
    poses_bounds = compute_pose_bounds(K_list, R_list, T_list)

    print(f"Saving to {output_path}")
    np.save(output_path, poses_bounds)


if __name__ == "__main__":
    main()
