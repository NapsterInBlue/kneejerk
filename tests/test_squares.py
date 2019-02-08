import pathlib
from unittest import TestCase

import cv2


HERE = pathlib.Path('.').resolve()
IM_DIR = HERE.joinpath('tests/images/')

TARGET_PATH = IM_DIR.joinpath('target_200_200.png')


class Test_Squares(TestCase):

    def test_behavior(self):
        result = cv2.imread(str(TARGET_PATH))
        print(result)
        print(result.shape)
