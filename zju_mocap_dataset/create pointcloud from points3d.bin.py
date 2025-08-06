import struct


def read_points3D_binary(path):
    Point3D = []
    with open(path, "rb") as f:
        while True:
            binary_data = f.read(48)
            if not binary_data or len(binary_data) < 48:
                break

            unpacked = struct.unpack("<Q3d4BdI", binary_data)
            point_id = unpacked[0]
            xyz = unpacked[1:4]
            rgb = unpacked[4:7]
            error = unpacked[8]
            track_length = unpacked[9]

            f.seek(track_length * 8, 1)

            Point3D.append({
                "id": point_id,
                "xyz": xyz,
                "rgb": rgb,
                "error": error,
                "track_length": track_length
            })
    return Point3D


def write_ply(points, ply_path):
    with open(ply_path, "w") as f:
        f.write("ply\n")
        f.write("format ascii 1.0\n")
        f.write(f"element vertex {len(points)}\n")
        f.write("property float x\n")
        f.write("property float y\n")
        f.write("property float z\n")
        f.write("property uchar red\n")
        f.write("property uchar green\n")
        f.write("property uchar blue\n")
        f.write("end_header\n")

        for p in points:
            x, y, z = p["xyz"]
            r, g, b = p["rgb"]
            f.write(f"{x} {y} {z} {r} {g} {b}\n")


if __name__ == "__main__":
    import sys

    sys.exit(1)

    if len(sys.argv) != 3:
        print("Usage: python convert_points3D_to_ply.py path/to/points3D.bin output.ply")
        exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    print(f"Reading points from {input_path}...")
    points = read_points3D_binary(input_path)
    print(f"Read {len(points)} points.")

    print(f"Writing to {output_path}...")
    write_ply(points, output_path)
    print("Done.")
