def GetIntrinsicMat(mode):
    if mode is 'nyu_color_standard_crop':
        fx_rgb = 5.1885790117450188e+02
        fy_rgb = 5.1946961112127485e+02
        cx_rgb = 3.2558244941119034e+02
        cy_rgb = 2.5373616633400465e+02
        K = [[fx_rgb, 0, cx_rgb-40],
             [0, fy_rgb, (cy_rgb-44)],
             [0, 0, 1]]

    return K


def get_3d_proposals(dmap, K, sp_base, sp_label, depth_fill, avg_boxDims_cls):
    # xyz camera coordinates
    xyz = Dmap2PointCloud(dmap, K)
    