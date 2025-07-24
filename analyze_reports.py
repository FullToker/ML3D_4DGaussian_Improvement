import os
import json
import re

def parse_results_json(json_path):
    if not os.path.exists(json_path):
        return {}
    with open(json_path, "r") as f:
        data = json.load(f)
    # only take the first method (usually only one)
    if isinstance(data, dict):
        for method in data:
            return data[method]
    return {}

def parse_report(report_path):
    result = {}
    if not os.path.exists(report_path):
        return result
    with open(report_path, "r") as f:
        for line in f:
            if line.startswith("Render test PSNR:"):
                m = re.match(r"Render test PSNR: ([\d.]+) L1: ([\d.]+)", line)
                if m:
                    result['psnr'] = float(m.group(1))
                    result['l1'] = float(m.group(2))
            elif line.startswith("Render test FPS:"):
                m = re.match(r"Render test FPS: ([\d.]+)", line)
                if m:
                    result['fps'] = float(m.group(1))
            elif line.startswith("Render video FPS:"):
                m = re.match(r"Render video FPS: ([\d.]+)", line)
                if m:
                    result['video_fps'] = float(m.group(1))
    return result

base_dir = "output/dnerf"
results = []

# find all scene and pruning_scene
for name in os.listdir(base_dir):
    if os.path.isdir(os.path.join(base_dir, name)) and not name.startswith("pruning_"):
        scene = name
        pruning_scene = f"pruning_{scene}"
        orig_json = os.path.join(base_dir, scene, "results.json")
        pruning_json = os.path.join(base_dir, pruning_scene, "results.json")
        orig_report = os.path.join(base_dir, scene, "report.txt")
        pruning_report = os.path.join(base_dir, pruning_scene, "report.txt")
        if os.path.exists(orig_json) and os.path.exists(pruning_json) and os.path.exists(orig_report) and os.path.exists(pruning_report):
            orig_metrics = parse_results_json(orig_json)
            pruning_metrics = parse_results_json(pruning_json)
            orig_fps = parse_report(orig_report)
            pruning_fps = parse_report(pruning_report)
            # merge
            orig = {**orig_metrics, **orig_fps}
            pruning = {**pruning_metrics, **pruning_fps}
            results.append((scene, orig, pruning))

# all metrics to compare
all_keys = set()
for _, orig, pruning in results:
    all_keys.update(orig.keys())
    all_keys.update(pruning.keys())
all_keys = sorted(list(all_keys))

output_file = os.path.join(base_dir, "analysis_report.txt")
with open(output_file, "w") as f:
    # unified header
    header = "Scene" + "".join([f"\t{key}" for key in all_keys]) + "\n"

    # Orig data
    f.write("Orig\n")
    f.write(header)
    for scene, orig, _ in results:
        f.write(scene)
        for key in all_keys:
            v = orig.get(key, 'NA')
            if isinstance(v, float):
                f.write(f"\t{v:.4f}")
            else:
                f.write(f"\t{v}")
        f.write("\n")

    # Pruning data
    f.write("\nPruning\n")
    f.write(header)
    for scene, _, pruning in results:
        f.write(scene)
        for key in all_keys:
            v = pruning.get(key, 'NA')
            if isinstance(v, float):
                f.write(f"\t{v:.4f}")
            else:
                f.write(f"\t{v}")
        f.write("\n")

    # Improvement table
    f.write("\nImprovement(%)\n")
    f.write(header)
    for idx, (scene, orig, pruning) in enumerate(results):
        f.write(scene)
        for key in all_keys:
            try:
                o = float(orig.get(key, 0))
                p = float(pruning.get(key, 0))
                if o != 0:
                    imp = (p - o) / o * 100
                    f.write(f"\t{imp:+.2f}")
                else:
                    f.write("\tNA")
            except Exception:
                f.write("\tNA")
        f.write("\n")

    # overall average
    if len(results) > 0:
        f.write("\nOverall Average:\n")
        f.write("Orig")
        for key in all_keys:
            avg = sum(float(orig.get(key, 0)) for _, orig, _ in results) / len(results)
            f.write(f"\t{avg:.4f}")
        f.write("\nPruning")
        for key in all_keys:
            avg = sum(float(pruning.get(key, 0)) for _, _, pruning in results) / len(results)
            f.write(f"\t{avg:.4f}")
        f.write("\nImprovement(%)")
        for key in all_keys:
            try:
                o_avg = sum(float(orig.get(key, 0)) for _, orig, _ in results) / len(results)
                p_avg = sum(float(pruning.get(key, 0)) for _, _, pruning in results) / len(results)
                if o_avg != 0:
                    imp = (p_avg - o_avg) / o_avg * 100
                    f.write(f"\t{imp:+.2f}")
                else:
                    f.write("\tNA")
            except Exception:
                f.write("\tNA")
        f.write("\n")
    else:
        f.write("No valid pairs found.\n")

print(f"Analysis report saved to {output_file}")