# 4D Gaussian Splatting - Motion/Transformation-based Pruning Improvements

## 1. What did I do?

This branch adds **redundant Gaussian point pruning acceleration** to the original 4D Gaussian Splatting:

- **Motion-based Pruning**: Tracks the deformation magnitude of each Gaussian point and automatically prunes points with low motion (almost static).
- **Transformation-based Pruning**: Prunes points with minimal scaling/rotation changes.
- **Dynamic Point Supplementation**: Automatically adds points when the total number is too low, preventing sparse point clouds from screwing up rendering.
- **All new pruning logic can be toggled via parameters and is compatible with the original pruning method.**

## 2. Main Parameters (`arguments/dnerf/pruning_bouncingballs.py`)

```python
OptimizationParams = dict(
    use_motion_pruning = True,           # Enable motion-based pruning (main switch)
    motion_prune_threshold = 0.01,       # Prune if deformation magnitude is below this threshold
    use_low_transform_pruning = True,    # Enable transformation-based pruning
    low_transform_threshold = 0.01,      # Prune if scaling/rotation change is below this threshold
    min_point_number = 10000,            # Auto-supplement if point count is too low
    supplement_point_number = 5000,      # Number of points to add each time
)
```

- To use only the original pruning, set `use_motion_pruning=False` and `use_low_transform_pruning=False`.
- To use the new pruning, set them to `True`.

## 3. Main Modified Files

- `arguments/dnerf/pruning_bouncingballs.py`  —— Parameter switches
- `scene/gaussian_model.py`  —— Pruning/supplementation/deformation accumulation logic
- `scene/deformation.py`     —— Deformation output dx
- `train.py`                 —— Main training loop calls new pruning

## 4. How to Start Training

### 1. Install Dependencies

```bash
# Recommended: use conda
conda create -n 4dgs python=3.8 -y
conda activate 4dgs
pip install -r requirements.txt
# You also need to compile simple_knn and other CUDA dependencies, see the original README
```

### 2. Training Command

Assuming you use the pruning_bouncingballs config:

```bash
python train.py --configs arguments/dnerf/pruning_bouncingballs.py --expname test_motion_pruning
```

- You can directly modify parameters in `pruning_bouncingballs.py`, or create your own config.
- Training logs, models, and point clouds will be automatically saved to `./output/test_motion_pruning/`.

### 3. Switch Between New and Old Pruning Logic

- **Use new pruning**: Set `use_motion_pruning=True` or `use_low_transform_pruning=True`
- **Use only original pruning**: Set both to `False`

## 5. Code Entry Points

- The main training loop is in `train.py` under `scene_reconstruction`.
- Pruning logic is in the `prune` method of `scene/gaussian_model.py`.
- Deformation tracking is in `scene/deformation.py` and `gaussian_model.py`.