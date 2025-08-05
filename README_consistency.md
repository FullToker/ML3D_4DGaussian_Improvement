# 4D Gaussian Splatting - Temporal Regularization & Evaluation Improvements

## 1. What did I do?

This branch adds **temporal consistency regularization and new evaluation metrics** to the original 4D Gaussian Splatting:

- **Temporal Consistency Regularization**: 
  - First-order finite difference 
  - Second-order finite difference
- **Finite-Difference Feature Loss**:
  - Penalizes changes in position, scale, and rotation across adjacent frames
- **Temporal Evaluation Metrics**: 
  - Optical Flow Smoothness (OFS)
  - Temporal MS-SSIM (T-MSSSIM)
  - Temporal LPIPS (T-LPIPS)

## 2. Main Parameters (`arguments/dnerf/reg_jumpingjacks.py`)

```python
OptimizationParams = dict(
    lambda_smooth1 = 0.002,       # 1st-order temporal smoothness
    lambda_smooth2 = 0.010,       # 2nd-order smoothness (acceleration)

    delta_t = 0.005,              # Frame interval, updated according to per-frame timestamp differences

    lambda_fd_means = 0.2,        # Finite-diff: position
    lambda_fd_scales = 0.2,       # Finite-diff: scale
    lambda_fd_rot = 0.1,          # Finite-diff: rotation
)
```

## 3. Main Modified Files

- `arguments/dnerf/reg_bouncingballs.py`  —— Hyperparameters
- `train.py`                 —— Contains all temporal consistency loss logic 
- `test_jitter.py`                 —— Evaluation: OFS, T-MSSSIM, T-LPIPS 
