from scidag.core._runnable import Runnable
from scidag.core.task import Task
from omegaconf import DictConfig


class DAG(Runnable):
    """
    Class to manupulate dags
    """

    def __init__(self, cfg: DictConfig) -> None:
        """
        Parameters
        ----------
        cfg : DictConfig
            _description_
        """

    @classmethod
    def build_from_cfg(cls, cfg: DictConfig):
        """
        Build `DAG` by provided config

        Parameters
        ----------
        cfg : DictConfig
            _description_
        """

    def get_task(self, name: str) -> Task:
        """Get Task by its name"""

    def run(self) -> None:
        """run dag with logging and saving in hydra"""
