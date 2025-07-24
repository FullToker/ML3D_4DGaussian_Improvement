from pathlib import Path
import os
from PIL import Image
import torch
import torchvision.transforms.functional as tf
from argparse import ArgumentParser
from tqdm import tqdm
from pytorch_msssim import ms_ssim
import torchvision.models.optical_flow as of  # RAFT
import torch.nn.functional as F
import json

def readImages(renders_dir, gt_dir):
    renders, gts, image_names = [], [], []
    for fname in sorted(os.listdir(renders_dir)):
        render_path = renders_dir / fname
        gt_path = gt_dir / fname
        if not gt_path.exists():
            raise FileNotFoundError(f"GT frame not found: {gt_path}")
        render = Image.open(render_path).convert("RGB")
        gt = Image.open(gt_path).convert("RGB")
        renders.append(tf.to_tensor(render).unsqueeze(0).cuda())
        gts.append(tf.to_tensor(gt).unsqueeze(0).cuda())
        image_names.append(fname)
    return renders, gts, image_names

def compute_temporal_msssim_simple(frames):
    if len(frames) < 2:
        return 1.0
    scores = []
    for i in range(len(frames) - 1):
        score = ms_ssim(frames[i], frames[i + 1], data_range=1, size_average=True)
        scores.append(score.item())
    return torch.tensor(scores).mean().item()

def compute_temporal_msssim_multi(frames, temporal_scales=[1, 2, 4]):
    if len(frames) < 2:
        return 1.0
    all_scores = []
    for dt in temporal_scales:
        if dt >= len(frames):
            continue
        for i in range(len(frames) - dt):
            score = ms_ssim(frames[i], frames[i + dt], data_range=1, size_average=True)
            all_scores.append(score.item())
    return torch.tensor(all_scores).mean().item() if all_scores else 1.0

# Opticalflow smoothness
@torch.no_grad()
def compute_opticalflow_smoothness(frames, flow_model):
    if len(frames) < 3:
        return 0.0
    prev_flow = None
    flow_diffs = []

    for i in range(len(frames) - 1):
        img1 = F.interpolate(frames[i], size=(224, 224), mode="bilinear")
        img2 = F.interpolate(frames[i+1], size=(224, 224), mode="bilinear")

        flow = flow_model(img1, img2)[-1]  #  final optical flow output
        if prev_flow is not None:
            diff = (flow - prev_flow).abs().mean().item()  #  adjacent optical flow
            flow_diffs.append(diff)
        prev_flow = flow

    return float(torch.tensor(flow_diffs).mean().item()) if flow_diffs else 0.0


def evaluate_t_metrics(model_paths):

    print("Loading RAFT optical flow model...")
    flow_model = of.raft_large(pretrained=True).eval().cuda()

    results_dict = {}

    for scene_dir in model_paths:
        print(f"\nScene: {scene_dir}")
        results_dict[scene_dir] = {}

        test_dir = Path(scene_dir) / "test"
        for method in os.listdir(test_dir):
            print(f"  Method: {method}")
            method_dir = test_dir / method
            gt_dir = method_dir / "gt"
            renders_dir = method_dir / "renders"

            renders, gts, _ = readImages(renders_dir, gt_dir)

            # Fast Frame-to-Frame
            t_simple_renders = compute_temporal_msssim_simple(renders)
            t_simple_gt = compute_temporal_msssim_simple(gts)

            # Standard Multi-Scale Δt=[1,2,4]
            t_multi_renders = compute_temporal_msssim_multi(renders, temporal_scales=[1,2,4])
            t_multi_gt = compute_temporal_msssim_multi(gts, temporal_scales=[1,2,4])

            # Opticalflow smoothness
            flow_smooth_renders = compute_opticalflow_smoothness(renders, flow_model)
            flow_smooth_gt = compute_opticalflow_smoothness(gts, flow_model)

            print(f"     T-MSSSIM-simple (renders): {t_simple_renders:.6f}")
            print(f"     T-MSSSIM-simple (GT): {t_simple_gt:.6f}")
            print(f"     T-MSSSIM-multi (renders): {t_multi_renders:.6f}")
            print(f"     T-MSSSIM-multi (GT): {t_multi_gt:.6f}")
            print(f"     OpticalFlow-Smoothness (renders): {flow_smooth_renders:.6f} ")
            print(f"     OpticalFlow-Smoothness (GT): {flow_smooth_gt:.6f} ")

            results_dict[scene_dir][method] = {
                "T-MSSSIM-renders-simple": t_simple_renders,
                "T-MSSSIM-GT-simple": t_simple_gt,
                "T-MSSSIM-renders-multi": t_multi_renders,
                "T-MSSSIM-GT-multi": t_multi_gt,
                "OpticalFlowSmooth-renders": flow_smooth_renders,
                "OpticalFlowSmooth-GT": flow_smooth_gt
            }

        out_json = Path(scene_dir) / "results_jitter.json"
        with open(out_json, 'w') as fp:
            json.dump(results_dict[scene_dir], fp, indent=2)
        print(f" Saved (T-MSSSIM + OpticalFlow) results to {out_json}")

    return results_dict

if __name__ == "__main__":
    device = torch.device("cuda:0")
    torch.cuda.set_device(device)

    parser = ArgumentParser(description="Temporal metrics (T-MSSSIM + OpticalFlow smoothness)")
    parser.add_argument('--model_paths', '-m', required=True, nargs="+", type=str, default=[])
    args = parser.parse_args()

    evaluate_t_metrics(args.model_paths)
