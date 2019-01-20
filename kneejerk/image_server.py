import os
import pathlib

import cv2
import matplotlib.pylab as plt


def do_all_processing(input_dir):

    input_dir_str = str(pathlib.Path(input_dir).resolve())
    fpaths = []
    scores = []

    for impath in os.listdir(input_dir):
        built_fpath = input_dir_str + impath
        fpaths.append(built_fpath)
        scores.append(score_image(impath))


def score_image(impath):

    fig = serve_image(impath)
    fig.canvas.mpl_connect('key_press_event', handle_keypress)

    # allows scoring/keying values
    # close the image
    pass



def serve_image(impath):
    with csv.imread(impath) as im_arr:
        im_arr = cv2.cvtColor(im_arr, cv2.COLOR_BGR2RGB)
        fig = plt.imshow(im)
    return fig



def handle_keypress(event):
    print('press', event.key)
    sys.stdout.flush()
    if event.key in [0, 1]:
        print('hey, it worked')


# handles saving/persisting of scores


