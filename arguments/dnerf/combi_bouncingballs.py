_base_ = './dnerf_default.py'

ModelHiddenParams = dict(
    kplanes_config = {
     'grid_dimensions': 2,
     'input_coordinate_dim': 4,
     'output_coordinate_dim': 32,
     'resolution': [64, 64, 64, 75]
    },

    lambda_smooth1 = 0.002,
    lambda_smooth2 = 0.010,
    delta_t = 0.0067,

    lambda_fd_means  = 0.002,
    lambda_fd_scales = 0.001,
    lambda_fd_rot    = 0.001
)


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
