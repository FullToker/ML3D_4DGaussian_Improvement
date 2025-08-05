_base_ = './bouncingballs.py'

ModelHiddenParams = dict(
    lambda_smooth1 = 0.002,
    lambda_smooth2 = 0.010,
    delta_t = 0.0067,

    lambda_fd_means  = 0.002,
    lambda_fd_scales = 0.001,
    lambda_fd_rot    = 0.001
)