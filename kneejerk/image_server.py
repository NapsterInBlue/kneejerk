import sys
import os
import pathlib
import random

import cv2
import click

import matplotlib
matplotlib.use('TkAgg')

import matplotlib.pylab as plt


fpaths = []
scores = []


def score_images_in_dir(input_dir, shuffle_files=True):
    """
    Given an input directory where images are located
    will serve up images for user scoring
    """
    input_dir_path = pathlib.Path(input_dir)

    files_in_dir = os.listdir(input_dir)
    if shuffle_files:
        random.shuffle(files_in_dir)

    for impath in files_in_dir:
        if str(impath[-4:]).lower() not in ['.png', '.jpg']:
            continue

        built_fpath = input_dir_path.joinpath(impath)

        fpaths.append(str(built_fpath.resolve()))
        score_image(built_fpath)

    return fpaths, scores


def score_image(impath):
    """
    Takes image path, displays the image,
    and connects keypress event to it
    """
    fig = serve_image(impath)
    fig.canvas.mpl_connect('key_press_event', handle_keypress)

    plt.show()


def serve_image(impath):
    """
    Load up image with cv2 with RGB rendering
    return the ``matplotlib.Figure`` object it
    yields
    """
    im_arr = cv2.imread(str(impath))
    im_arr = cv2.cvtColor(im_arr, cv2.COLOR_BGR2RGB)

    fig = plt.imshow(im_arr).figure
    return fig


@click.pass_context
def handle_keypress(ctx, event):
    """
    When user keys in a correct input, appends
    to the global ``scores`` variable
    """
    min_val = ctx.obj['min_val']
    max_val = ctx.obj['max_val']
    sys.stdout.flush()

    acceptable_vals = set(map(str, range(int(min_val), int(max_val)+1)))
    if event.key in acceptable_vals:
        plt.close()
        scores.append(int(event.key))
    else:
        print(f'Acceptable keystrokes are in [{min_val}, {max_val}]')
        sys.stdout.flush()