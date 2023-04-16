from datetime import datetime
import os


def create_path(subdir: str | None = None):
    dtm = datetime.now().strftime("%d-%m-%Y_%H-%M")
    # TODO: Rewrite
    path_dir = os.path.join("configs", str(dtm))
    if subdir is not None:
        path_dir = os.path.join(path_dir, subdir)
    if not os.path.isdir(path_dir):
        os.makedirs(path_dir)
    return path_dir
