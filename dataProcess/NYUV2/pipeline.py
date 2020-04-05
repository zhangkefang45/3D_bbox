import scipy.io as scio
import dataProcess.NYUV2.function as fuc
import numpy as np
FILE_LEN = 1500

def get_dmap_f():
    # For NYU dataset v2
    # convert dmap to [0, 255], where 255 represents 10 meters


    data_path = "D:\\Study\\3D_bbox\\dataset\\NYUV2\\dmap_f\\"
    save_path = "D:\\Study\\3D_bbox\\dataProcess\\NYUV2\\dmap_f\\"
    for i in range(1, FILE_LEN):
        file_name = str(i) + ".mat"
        full_path = data_path + file_name
        data = scio.loadmat(full_path)
        dmap_f = data['dmap_f']

        mask = [dmap_f > 10]
        dmap_f[tuple(mask)] = 10
        dmap_f = dmap_f/10 * 255
        scio.savemat(save_path + file_name, {"dmap_f": dmap_f})

def get_proposals():
    # compute proposals for both 2D and 3D

    dataset_path = "D:\\Study\\3D_bbox\\dataset\\NYUV2\\"
    process_path = "D:\\Study\\3D_bbox\\dataProcess\\NYUV2\\"

    # detection classes
    det_calsses =  {'bathtub',  'bed', 'bookshelf', 'box', 'chair', 'counter',
               'desk', 'door', 'dresser', 'garbage bin', 'lamp',
               'monitor', 'night stand', 'pillow', 'sink', 'sofa',
               'table', 'television', 'toilet'}

    # average box dimensions
    data = scio.loadmat(dataset_path + 'classwise_bboxDims.mat')

    # intrinsic matrix
    K = fuc.GetIntrinsicMat('nyu_color_standard_crop')

    for i in range(1, FILE_LEN):
        imPackName = "NYUV%.4d" % (i)
        print(imPackName)

        # 2d proposals (format: [xmin, ymin, xmax, ymax], start at 0)
        var = scio.loadmat(process_path + "Segs" + imPackName + 'candidates.mat')
        candidates = var['candidates']
        bbox_2d = candidates['bboxes']
        boxes = bbox_2d[:, [2,1,4,3]] - 1

        # remove rois whos area is less than 200 pixels
        w = boxes[:, 3] - boxes[:, 1] + 1
        h = boxes[:, 4] - boxes[:, 2] + 1
        A = np.multiply(w,h)
        valid = A>=200
        boxes2d_prop = boxes[valid, :]
        scio.savemat(process_path + 'proposal2d' + str(i) + 'mat', {"boxes2d_prop":boxes2d_prop})

        # 3d proposals
        sp_base = candidates['superpixels']
        sp_label = candidates['labels']
        sp_label = sp_label[valid]

        # load hole-filled depth map
        data = scio.loadmat(dataset_path + "dmap_f\\" + str(i) + ".mat")
        dmap_f = data['dmap_f']
        depth_fill = float(dmap_f)

        # load original map
        data = scio.loadmat(dataset_path + "rawDepth\\" + str(i) + ".mat")
        rawDepth = data['rawDepth']

        boxes3d_prop =

def extract_GTInfo():
    pass


def get_gt_overlaps():
    pass


if __name__ == "__main__":
    # depth image
    # get_dmap_f()

    # proposals
    get_proposals()

    # ground truths
    extract_GTInfo()
    get_gt_overlaps()