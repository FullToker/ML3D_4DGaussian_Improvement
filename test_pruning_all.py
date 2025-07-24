import os
import shutil

# 1. generate pruning version of config
pruning_params = """
OptimizationParams = dict(
    use_motion_pruning = True,
    low_motion_threshold = 0.08,
    use_low_transform_pruning = True,
    low_transform_threshold = 0.08,
    min_point_number = 10000,
    supplement_point_number = 5000,
    pruning_from_iter = 1000,
    pruning_interval = 200,
)
"""

config_dir = "arguments/dnerf"
for fname in os.listdir(config_dir):
    if fname.endswith(".py") and not fname.startswith("pruning_"):
        src = os.path.join(config_dir, fname)
        dst = os.path.join(config_dir, "pruning_" + fname)
        with open(src, "r") as f:
            content = f.read()
        # if OptimizationParams is in the content, replace it with pruning_params
        if "OptimizationParams" in content:
            content = content.split("OptimizationParams")[0] + pruning_params
        else:
            content = content.strip() + "\n\n" + pruning_params
        with open(dst, "w") as f:
            f.write(content)
        print(f"Generated {dst}")

# 2. run all experiments
data_dir = "data"
scene_list = [d for d in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, d))]

for scene in scene_list:
    expname = f"dnerf/{scene}"
    pruning_expname = f"dnerf/pruning_{scene}"

    config_path = os.path.join(config_dir, f"{scene}.py")
    pruning_config_path = os.path.join(config_dir, f"pruning_{scene}.py")
    output_path = os.path.join("output/dnerf", scene)
    pruning_output_path = os.path.join("output/dnerf", f"pruning_{scene}")

    os.system(f"python train.py -s {data_dir}/{scene} --expname {expname} --configs {config_path}")
    os.system(f"python train.py -s {data_dir}/{scene} --expname {pruning_expname} --configs {pruning_config_path}")
    
    os.system(f"python render.py --model_path {output_path}/ --skip_train --configs {config_path}")
    os.system(f"python render.py --model_path {pruning_output_path}/ --skip_train --configs {pruning_config_path}")
    
    print(f"Done {expname} and {pruning_expname}")

print("All done.")