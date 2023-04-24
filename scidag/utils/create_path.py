import os
from datetime import datetime


def create_path():
    dtm = datetime.now().strftime("%d-%m-%Y_%H-%M")
    # TODO: Rewrite
    path_dir = os.path.join("configs", str(dtm))
    if not os.path.isdir(path_dir):
        os.makedirs(path_dir)
    return path_dir
