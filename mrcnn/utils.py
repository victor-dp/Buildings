"""
Mask R-CNN
Common utility functions and classes.

Copyright (c) 2017 Matterport, Inc.
Licensed under the MIT License (see LICENSE for details)
Written by Waleed Abdulla
"""

import numpy as np
import scipy.misc
import scipy.ndimage


import os
import random
import colorsys
from skimage.measure import find_contours
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Polygon

import pdb

from functools import wraps


def debug(func):
    """Python wraps."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        print("[DEBUG] {}(): ".format(func.__name__))
        # print("  ", args, kwargs)
        return func(*args, **kwargs)
    return wrapper


if "DISPLAY" not in os.environ:
    plt.switch_backend('agg')


def resize_image(image, min_dim=None, max_dim=None, padding=False):
    """
    Resize an image keeping the aspect ratio.

    min_dim: if provided, resizes the image such that it's smaller
        dimension == min_dim
    max_dim: if provided, ensures that the image longest side doesn't
        exceed this value.
    padding: If true, pads image with zeros so it's size is max_dim x max_dim

    Returns:
    image: the resized image
    window: (y1, x1, y2, x2). If max_dim is provided, padding might
        be inserted in the returned image. If so, this window is the
        coordinates of the image part of the full image (excluding
        the padding). The x2, y2 pixels are not included.
    scale: The scale factor used to resize the image
    padding: Padding added to the image [(top, bottom), (left, right), (0, 0)]
    """
    # Default window (y1, x1, y2, x2) and default scale == 1.
    h, w = image.shape[:2]
    window = (0, 0, h, w)
    scale = 1

    # Scale?
    if min_dim:
        # Scale up but not down
        scale = max(1, min_dim / min(h, w))
    # Does it exceed max dim?
    if max_dim:
        image_max = max(h, w)
        if round(image_max * scale) > max_dim:
            scale = max_dim / image_max
    # Resize image and mask
    if scale != 1:
        image = scipy.misc.imresize(
            image, (round(h * scale), round(w * scale)))
    # Need padding?
    if padding:
        # Get new height and width
        h, w = image.shape[:2]
        top_pad = (max_dim - h) // 2
        bottom_pad = max_dim - h - top_pad
        left_pad = (max_dim - w) // 2
        right_pad = max_dim - w - left_pad
        padding = [(top_pad, bottom_pad), (left_pad, right_pad), (0, 0)]
        image = np.pad(image, padding, mode='constant', constant_values=0)
        window = (top_pad, left_pad, h + top_pad, w + left_pad)
    return image, window, scale, padding


def unmold_mask(mask, bbox, image_shape):
    """Convert a mask generated by the neural network.

    mask: [height, width] of type float. A small, typically 28x28 mask.
    bbox: [y1, x1, y2, x2]. The box to fit the mask in.
    Returns a binary mask with the same size as the original image.
    """
    threshold = 0.5
    y1, x1, y2, x2 = bbox
    mask = scipy.misc.imresize(
        mask, (y2 - y1, x2 - x1), interp='bilinear').astype(np.float32) / 255.0
    mask = np.where(mask >= threshold, 1, 0).astype(np.uint8)

    # Put the mask in the right location.
    full_mask = np.zeros(image_shape[:2], dtype=np.uint8)
    full_mask[y1:y2, x1:x2] = mask
    return full_mask


############################################################
#  Anchors
############################################################

def create_anchors(scales, ratios, shape, feature_stride, anchor_stride):
    """Create anchors.

    scales: 1D array of anchor sizes in pixels. Example: [32, 64, 128]
    ratios: 1D array of anchor ratios of width/height. Example: [0.5, 1, 2]
    shape: [height, width] spatial shape of the feature map over which
            to generate anchors.
    feature_stride: Stride of the feature map relative to the image in pixels.
    anchor_stride: Stride of anchors on the feature map. For example, if the
        value is 2 then generate anchors for every other feature map pixel.
    """
    # Get all combinations of scales and ratios

    # pdb.set_trace()
    # (Pdb) a
    # scales = 32
    # ratios = [0.5, 1, 2]
    # shape = array([256, 256])
    # feature_stride = 4
    # anchor_stride = 1

    scales, ratios = np.meshgrid(np.array(scales), np.array(ratios))
    scales = scales.flatten()
    ratios = ratios.flatten()
    # (Pdb) scales
    # array([32, 32, 32])
    # (Pdb) ratios
    # array([ 0.5,  1. ,  2. ])

    # Enumerate heights and widths from scales and ratios
    heights = scales / np.sqrt(ratios)
    widths = scales * np.sqrt(ratios)
    # (Pdb) heights
    # array([ 45.254834,  32.      ,  22.627417])
    # (Pdb) widths
    # array([ 22.627417,  32.      ,  45.254834])

    # Enumerate shifts in feature space
    shifts_y = np.arange(0, shape[0], anchor_stride) * feature_stride
    shifts_x = np.arange(0, shape[1], anchor_stride) * feature_stride
    shifts_x, shifts_y = np.meshgrid(shifts_x, shifts_y)

    # Enumerate combinations of shifts, widths, and heights
    box_widths, box_centers_x = np.meshgrid(widths, shifts_x)
    box_heights, box_centers_y = np.meshgrid(heights, shifts_y)
    # (Pdb) box_widths.shape
    # (65536, 3)
    # (Pdb) box_widths
    # array([[ 22.627417,  32.      ,  45.254834],
    #        [ 22.627417,  32.      ,  45.254834],
    #        [ 22.627417,  32.      ,  45.254834],
    #        ...,
    #        [ 22.627417,  32.      ,  45.254834],
    #        [ 22.627417,  32.      ,  45.254834],
    #        [ 22.627417,  32.      ,  45.254834]])
    # (Pdb) box_heights.shape
    # (65536, 3)
    # (Pdb) bh
    # array([ 45.254834,  32.      ,  22.627417])
    # deltas=box_heights - bh
    # (Pdb) deltas.min(), deltas.max()
    # (-4.0609648976897006e-09, 0.0)

    # (Pdb) box_heights
    # array([[ 45.254834,  32.      ,  22.627417],
    #        [ 45.254834,  32.      ,  22.627417],
    #        [ 45.254834,  32.      ,  22.627417],
    #        ...,
    #        [ 45.254834,  32.      ,  22.627417],
    #        [ 45.254834,  32.      ,  22.627417],
    #        [ 45.254834,  32.      ,  22.627417]])

    # Reshape to get a list of (y, x) and a list of (h, w)
    box_centers = np.stack(
        [box_centers_y, box_centers_x], axis=2).reshape([-1, 2])
    # (Pdb) box_centers.shape
    # (196608, 2)
    # (Pdb) box_centers_y
    # array([[   0,    0,    0],
    #        [   0,    0,    0],
    #        [   0,    0,    0],
    #        ...,
    #        [1020, 1020, 1020],
    #        [1020, 1020, 1020],
    #        [1020, 1020, 1020]])
    # (Pdb) box_centers_x
    # array([[   0,    0,    0],
    #        [   4,    4,    4],
    #        [   8,    8,    8],
    #        ...,
    #        [1012, 1012, 1012],
    #        [1016, 1016, 1016],
    #        [1020, 1020, 1020]])
    # (Pdb) box_centers_x.shape,  box_centers_y.shape
    # ((65536, 3), (65536, 3))

    box_sizes = np.stack([box_heights, box_widths], axis=2).reshape([-1, 2])
    # (Pdb) np.unique(box_sizes.astype(int))
    # array([22, 32, 45])

    # Convert to corner coordinates (y1, x1, y2, x2)
    boxes = np.concatenate([box_centers - 0.5 * box_sizes,
                            box_centers + 0.5 * box_sizes], axis=1)

    return boxes


def create_pyramid_anchors(scales, ratios, feature_shapes, feature_strides, anchor_stride):
    """Generate anchors at different levels of a feature pyramid.

    Each scale
    is associated with a level of the pyramid, but each ratio is used in
    all levels of the pyramid.

    Returns:
    anchors: [N, (y1, x1, y2, x2)]. All generated anchors in one array. Sorted
        with the same order of the given scales. So, anchors of scale[0] come
        first, then anchors of scale[1], and so on.
    """
    # Anchors
    # [anchor_count, (y1, x1, y2, x2)]
    anchors = []
    for i in range(len(scales)):
        anchors.append(
            create_anchors(scales[i], ratios, feature_shapes[i], feature_strides[i],
                           anchor_stride))

    # scales = array([32, 32, 32])
    # ratios = array([ 0.5,  1. ,  2. ])
    # shape = array([256, 256])
    # feature_stride = 4
    # anchor_stride = 1
    # (Pdb) boxes.shape
    # (196608, 4)

    # (Pdb) a
    # scales = array([64, 64, 64])
    # ratios = array([ 0.5,  1. ,  2. ])
    # shape = array([128, 128])
    # feature_stride = 8
    # anchor_stride = 1
    # (Pdb) boxes.shape
    # (49152, 4)

    # (Pdb) a
    # scales = array([128, 128, 128])
    # ratios = array([ 0.5,  1. ,  2. ])
    # shape = array([64, 64])
    # feature_stride = 16
    # anchor_stride = 1
    # (Pdb)  boxes.shape
    # (12288, 4)

    # (Pdb) a
    # scales = array([256, 256, 256])
    # ratios = array([ 0.5,  1. ,  2. ])
    # shape = array([32, 32])
    # feature_stride = 32
    # anchor_stride = 1
    # (Pdb) (Pdb)  boxes.shape
    # (Pdb) (3072, 4)

    # (Pdb) a
    # scales = array([512, 512, 512])
    # ratios = array([ 0.5,  1. ,  2. ])
    # shape = array([16, 16])
    # feature_stride = 64
    # anchor_stride = 1
    # (Pdb) boxes.shape
    # (768, 4)
    # (Pdb)

    # (Pdb) 196608 + 49152 + 12288 + 3072 + 768
    # 261888

    return np.concatenate(anchors, axis=0)


def random_colors(N, bright=True):
    """Generate random colors.

    To get visually distinct colors, generate them in HSV space then
    convert to RGB.
    """
    brightness = 1.0 if bright else 0.7
    hsv = [(i / N, 1, brightness) for i in range(N)]
    colors = list(map(lambda c: colorsys.hsv_to_rgb(*c), hsv))
    random.shuffle(colors)
    return colors


def apply_mask(image, mask, color, alpha=0.5):
    """Apply the given mask to the image."""
    # pdb.set_trace()
    # (Pdb) image.shape
    # (1200, 1920, 3)
    # (Pdb) mask.shape
    # (1024, 1024)

    for c in range(3):
        image[:, :, c] = np.where(
            mask == 1, image[:, :, c] * (1 - alpha) + alpha * color[c] * 255,
            image[:, :, c])
    return image


def display_instances(image, boxes, masks, class_ids, class_names,
                      scores=None, title="",
                      figsize=(16, 16), ax=None):
    """
    Display instances.

    boxes: [num_instance, (y1, x1, y2, x2, class_id)] in image coordinates.
    masks: [num_instances, height, width]
    class_ids: [num_instances]
    class_names: list of class names of the dataset
    scores: (optional) confidence scores for each box
    figsize: (optional) the size of the image.
    """
    # Number of instances
    # pdb.set_trace()
    # (Pdb) type(image)
    # <class 'numpy.ndarray'>
    # (Pdb) image.shape
    # (1200, 1920, 3)

    N = len(boxes)
    if not N:
        print("\n*** No instances to display *** \n")

    if not ax:
        _, ax = plt.subplots(1, figsize=figsize)

    # Generate random colors
    colors = random_colors(N)

    # Show area outside image boundaries.
    height, width = image.shape[:2]
    ax.set_ylim(height + 10, -10)
    ax.set_xlim(-10, width + 10)
    ax.axis('off')
    ax.set_title(title)

    masked_image = image.astype(np.uint32).copy()
    for i in range(N):
        color = colors[i]

        # Bounding box
        if not np.any(boxes[i]):
            # Skip this instance. Has no bbox. Likely lost in image cropping.
            continue
        y1, x1, y2, x2 = boxes[i]
        p = patches.Rectangle((x1, y1), x2 - x1, y2 - y1, linewidth=1,
                              alpha=0.7, linestyle="dashed",
                              edgecolor=color, facecolor='none')
        ax.add_patch(p)

        # Label
        score = scores[i] if scores is not None else None
        label = class_names[i]
        # x = random.randint(x1, (x1 + x2) // 2)
        caption = "{} {:.3f}".format(label, score) if score else label
        ax.text(x1, y1 + 10, caption,
                color='w', size=11, backgroundcolor="none")

        # Mask
        mask = masks[i, :, :]
        masked_image = apply_mask(masked_image, mask, color, alpha=0.1)

        # Mask Polygon
        # Pad to ensure proper polygons for masks that touch image edges.
        padded_mask = np.zeros(
            (mask.shape[0] + 2, mask.shape[1] + 2), dtype=np.uint8)
        padded_mask[1:-1, 1:-1] = mask
        contours = find_contours(padded_mask, 0.5)
        for verts in contours:
            # Subtract the padding and flip (y, x) to (x, y)
            verts = np.fliplr(verts) - 1
            p = Polygon(verts, facecolor="none", edgecolor=color)
            ax.add_patch(p)
    ax.imshow(masked_image.astype(np.uint8))

    plt.show()


def plot_loss(loss, val_loss, save=True, log_dir=None):
    """Plot loss."""
    loss = np.array(loss)
    val_loss = np.array(val_loss)

    plt.figure("loss")
    plt.gcf().clear()
    plt.plot(loss[:, 0], label='train')
    plt.plot(val_loss[:, 0], label='valid')
    plt.xlabel('epoch')
    plt.ylabel('loss')
    plt.legend()
    if save:
        save_path = os.path.join(log_dir, "loss.png")
        plt.savefig(save_path)
    else:
        plt.show(block=False)
        plt.pause(0.1)

    plt.figure("rpn_class_loss")
    plt.gcf().clear()
    plt.plot(loss[:, 1], label='train')
    plt.plot(val_loss[:, 1], label='valid')
    plt.xlabel('epoch')
    plt.ylabel('loss')
    plt.legend()
    if save:
        save_path = os.path.join(log_dir, "rpn_class_loss.png")
        plt.savefig(save_path)
    else:
        plt.show(block=False)
        plt.pause(0.1)

    plt.figure("rpn_bbox_loss")
    plt.gcf().clear()
    plt.plot(loss[:, 2], label='train')
    plt.plot(val_loss[:, 2], label='valid')
    plt.xlabel('epoch')
    plt.ylabel('loss')
    plt.legend()
    if save:
        save_path = os.path.join(log_dir, "rpn_bbox_loss.png")
        plt.savefig(save_path)
    else:
        plt.show(block=False)
        plt.pause(0.1)

    plt.figure("mrn_class_loss")
    plt.gcf().clear()
    plt.plot(loss[:, 3], label='train')
    plt.plot(val_loss[:, 3], label='valid')
    plt.xlabel('epoch')
    plt.ylabel('loss')
    plt.legend()
    if save:
        save_path = os.path.join(log_dir, "mrn_class_loss.png")
        plt.savefig(save_path)
    else:
        plt.show(block=False)
        plt.pause(0.1)

    plt.figure("mrn_bbox_loss")
    plt.gcf().clear()
    plt.plot(loss[:, 4], label='train')
    plt.plot(val_loss[:, 4], label='valid')
    plt.xlabel('epoch')
    plt.ylabel('loss')
    plt.legend()
    if save:
        save_path = os.path.join(log_dir, "mrn_bbox_loss.png")
        plt.savefig(save_path)
    else:
        plt.show(block=False)
        plt.pause(0.1)

    plt.figure("mrn_mask_loss")
    plt.gcf().clear()
    plt.plot(loss[:, 5], label='train')
    plt.plot(val_loss[:, 5], label='valid')
    plt.xlabel('epoch')
    plt.ylabel('loss')
    plt.legend()
    if save:
        save_path = os.path.join(log_dir, "mrn_mask_loss.png")
        plt.savefig(save_path)
    else:
        plt.show(block=False)
        plt.pause(0.1)
