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

### Temporal Smoothness Regularization (or something) 

1. Modify the loss function in the deformation MLP
2. Add finite-difference loss between Gaussians at adjacent frames
3. Cluster similar Gaussians by features to encourage motion consistency

### Supersampling Render Function for Anti-Aliasing

1. Increases Render Resolution
2. Downsamples with Averaging
