# ML3D_4DGaussian_Improvement
ML3D 25SS Project, about 4D Gaussian and its improvements
## Topic: Dynamic 3D Reconstruction from Multi-View Videos via 4D Gaussian Splatting
[Source Code](https://github.com/hustvl/4DGaussians)

## Datasets
1. [DynamicNeRF](https://github.com/gaochen315/DynamicNeRF): Dynamic View Synthesis from Dynamic Monocular Video
2. [ZJU-MoCap](https://chingswy.github.io/Dataset-Demo/) Dataset (no depth information)
3. [TUM RGB-D Dynamic Scenes Dataset](https://cvg.cit.tum.de/data/datasets/rgbd-dataset)

## Modifications
### Redundant Gaussian Pruning
1. Track deformation magnitude over time
2. Prune low-opacity and low-motion Gaussians, resample Gaussians in high-error areas
3. Add a dynamic density control module to the training loop

### Temporal Smoothness Regularization

1. Modify the loss function in the deformation MLP
2. Add finite-difference loss between Gaussians at adjacent frames
3. Cluster similar Gaussians by features to encourage motion consistency
