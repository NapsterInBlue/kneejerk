from pathlib import Path
import os


def _ensure_path_exists(fpath):
    try:
        os.makedirs(fpath)
    except FileExistsError:
        pass
