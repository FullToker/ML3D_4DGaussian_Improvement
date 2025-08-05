# ML3D_4DGaussian_Improvement
ML3D 25SS Project, about 4D Gaussian and its improvements
## Topic: Dynamic 3D Reconstruction from Multi-View Videos via 4D Gaussian Splatting
[Source Code](https://github.com/hustvl/4DGaussians)

## Datasets
[ZJU-MoCap](https://chingswy.github.io/Dataset-Demo/) Dataset

## Modifications
### Intelligent Dynamic Point Cloud Pruning
1. Analyze motion characteristics of each Gaussian point
2. Implement Motion-aware Pruning
3. Implement Transformation-aware Pruning

### Temporal Smoothness Regularization

1. Modify the loss function in the deformation MLP
2. Add finite-difference loss between Gaussians at adjacent frames

### Supersampling Render Function for Anti-Aliasing

1. Increases Render Resolution
2. Downsamples with Averaging

## How To Train
This project uses the same command-line interfaces as the original, but with different configuration parameters, e.g.,

Training on the synthetic D-NeRF dataset:

```bash
python train.py -s data/dnerf/bouncingballs --port 6017 --expname "dnerf/bouncingballs" --configs arguments/dnerf/combi_bouncingballs.py 
```

Training on the new ZJU-MoCap dataset:

```bash
python train.py -s zju_dataset/ --port 6017 --expname "zju_dataset" --configs arguments/dnerf/combi_bouncingballs.py
```

Rendering:

```bash
python render.py --model_path "output/dnerf/bouncingballs/"  --skip_train --configs arguments/dnerf/combi_bouncingballs.py 
```

Evaluation:

```bash
python metrics.py --model_path "output/dnerf/bouncingballs/" 
```

Evaluation using the newly introduced metrics:

```bash
python test_jitter.py --model_path "output/dnerf/bouncingballs/" 
```
