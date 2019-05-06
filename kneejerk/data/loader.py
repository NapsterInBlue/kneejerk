import cv2
import numpy as np


def load_normalized_image_data(fpath, consider_size=False, rescale_len=200):
    """
    Given a csv with columns (image filepath, numeric score)
    convert a series of images to numpy arrays (with some
    pre-processing) as well as their corresponding target values

    By default, the pre-processing is as follows:

    1. Go through and pad each non-square image with black
       until its height equals its width
    2. Downscale each image according to rescale_len

    Parameters
    ----------
    fpath: str, pathlike
        Location of the csv you want to read from
    consider_size: bool
        False: Each image follows the default behavior
               outlined above
        True:  Each image will be black-padded to be an NxN
               square, where N is the longest width/height
               found in the directory
    rescale_len: int
        The resulting images will each be of size
        (rescale_len, rescale_len)

    Returns
    -------
    X: numpy.array
        The numpy representation for each image in (R, G, B)
    y: numpy.array
        A float32 array of the target values for each image
    """

    max_image_dim = _get_max_image_dim(fpath)

    X = []
    y = []

    with open(fpath) as f:
        for row in f:
            impath, score = row.split(',')

            if consider_size:
                im = load_and_pad_images(impath, max_image_dim)
            else:
                im = load_and_pad_images(impath)


            im = cv2.resize(im, (rescale_len, rescale_len))
            X.append(im)
            y.append(float(score))

    X = np.array(X)
    y = np.array(y)

    return X, y


def load_and_pad_images(impath, max_image_dim=None):
    """
    Iterate though all of the image filepaths, load the
    images, then pad them with black, if necessary
    """
    imBGR = cv2.imread(impath)
    im = cv2.cvtColor(imBGR, cv2.COLOR_BGR2RGB)

    if not max_image_dim:
        max_image_dim = max(im.shape)

    height_needed, width_needed = _determine_pad_amount(im, max_image_dim,
                                                        max_image_dim)

    im = np.pad(im, ((0, height_needed), (0, width_needed), (0, 0)),
                mode='constant', constant_values=0)

    return im


def _get_max_image_dim(fpath):
    """
    Open up all of the images to see their heights and widths.
    Keep a running max of each, which is returned at the end.
    """

    max_height = 0
    max_width = 0

    with open(fpath) as f:
        for row in f:
            im_path = row.split(',')[0]
            im = cv2.imread(im_path)
            height, width, _ = im.shape

            if height > max_height:
                max_height = height

            if width > max_width:
                max_width = width

    print('Max height:', max_height)
    print('Max width :', max_width)

    return max(max_height, max_width)


def _determine_pad_amount(image_array, max_height, max_width):
    """
    Given an image and desired max height/width,
    find how much height and width is needed to make
    the image the appropriate size
    """

    height, width, _ = image_array.shape

    height_needed = max_height - height
    width_needed = max_width - width

    return height_needed, width_needed
