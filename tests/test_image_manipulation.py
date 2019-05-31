import pathlib
from unittest import TestCase

import cv2
import numpy as np

from kneejerk.data.transfer import load_and_pad_images
from kneejerk.data.utils import _get_max_image_dim


HERE = pathlib.Path('.').resolve()
IM_DIR = HERE.joinpath('tests/images/')


class TestSquares(TestCase):

    def test_small_to_big(self):
        result = load_and_pad_images(str(IM_DIR) + '/200_200.png', 400)
        expected = cv2.imread(str(IM_DIR) + '/200_200_target.png')

        np.testing.assert_equal(result, expected)

    def test_pad_right(self):
        result = load_and_pad_images(str(IM_DIR) + '/400_200.png', 400)
        expected = cv2.imread(str(IM_DIR) + '/400_200_target.png')

        np.testing.assert_equal(result, expected)

    def test_pad_bottom(self):
        result = load_and_pad_images(str(IM_DIR) + '/200_400.png', 400)
        expected = cv2.imread(str(IM_DIR) + '/200_400_target.png')

        np.testing.assert_equal(result, expected)

    def test_no_pad(self):
        result = load_and_pad_images(str(IM_DIR) + '/400_400.png', 400)
        expected = cv2.imread(str(IM_DIR) + '/400_400.png')

        np.testing.assert_equal(result, expected)


class TestFindDims(TestCase):
    def test_biggest_dim(self):
        print(HERE)
        max_image_dim = _get_max_image_dim(str(HERE) + '/tests/squares.csv')
        assert max_image_dim == 400

