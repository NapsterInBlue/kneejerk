import sys
import os
import pathlib
import csv

import cv2

import matplotlib
matplotlib.use('TkAgg')

import matplotlib.pylab as plt


def do_all_processing(input_dir):

    input_dir_path = pathlib.Path(input_dir)

    fpaths = []
    scores = []

    for impath in os.listdir(input_dir):
        print(str(impath))

        if str(impath[-4:]).lower() not in ['.png', '.jpg']:
            continue

        built_fpath = input_dir_path.joinpath(impath)

        fpaths.append(str(built_fpath.resolve()))
        scores.append(score_image(built_fpath))

    return fpaths, scores

def score_image(impath):

    fig = serve_image(impath)
    fig.canvas.mpl_connect('key_press_event', handle_keypress)

    plt.show()
    # allows scoring/keying values
    # close the image
    pass



def serve_image(impath):
    im_arr = cv2.imread(str(impath))
    im_arr = cv2.cvtColor(im_arr, cv2.COLOR_BGR2RGB)

    fig = plt.imshow(im_arr).figure
    return fig



def handle_keypress(event):
    print('press', event.key)
    sys.stdout.flush()
    if event.key in ['0', '1']:
        plt.close()

# handles saving/persisting of scores


