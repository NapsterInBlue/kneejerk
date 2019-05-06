import os
import cv2
import click
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

from kneejerk.data.utils import _get_max_image_dim, _determine_pad_amount


@click.pass_context
def segment_data_from_csv(ctx, trainpct, testpct, valpct):
    """
    Load the csv generated by `kneejerk score` and stratify into
    test, train, and validation DataFrames, per the parameters
    provided in `kneejerk transfer`

    :return: train, test, cross_val DataFrames
    """
    file_name = ctx.obj['file_name']

    df = pd.read_csv(file_name, names=['path', 'score'])

    train, test = train_test_split(df, test_size=testpct+valpct, stratify=df['score'])

    if valpct:
        # rescale the original pct
        valpct = (valpct / (1 - trainpct))
        test, cross_val = train_test_split(test, test_size=valpct, stratify=test['score'])
    else:
        cross_val = None

    return train, test, cross_val


@click.pass_context
def transfer_normalized_image_data(ctx, df, train_test_val, consider_size=False, rescale_len=200):
    """
    Given a DataFrame with columns (image filepath, numeric score)
    convert a series of images to numpy arrays (with some
    pre-processing) as well as their corresponding target values

    By default, the pre-processing is as follows:

    1. Go through and pad each non-square image with black
       until its height equals its width
    2. Downscale each image according to rescale_len

    Parameters
    ----------
    df: pandas.DataFrame
    train_test_val: str
        Whether we're saving the data in 'train', 'test',
        or 'val' directories
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

    dirname = ctx.obj['dirname']
    max_image_dim = ctx.obj['max_image_dim']

    for _, row in df.iterrows():
        impath, score = row

        if consider_size:
            im = load_and_pad_images(impath, max_image_dim)
        else:
            im = load_and_pad_images(impath)

        im = cv2.resize(im, (rescale_len, rescale_len))

        imname = impath.split(os.sep)[-1]
        fpath = os.path.join(dirname, train_test_val, str(score), imname)
        cv2.imwrite(fpath, im)


def load_and_pad_images(impath, max_image_dim=None):
    """
    Iterate though all of the image filepaths, load the
    images, then pad them with black, if necessary
    """
    im = cv2.imread(impath)

    if not max_image_dim:
        max_image_dim = max(im.shape)

    height_needed, width_needed = _determine_pad_amount(im, max_image_dim,
                                                        max_image_dim)

    im = np.pad(im, ((0, height_needed), (0, width_needed), (0, 0)),
                mode='constant', constant_values=0)

    return im

