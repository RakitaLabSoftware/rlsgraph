from omegaconf import DictConfig, OmegaConf

from scidag.core.node import Node


def test_task_run():
    cfg: DictConfig = OmegaConf.load(path)
    dummy_val = "dummy"
    node = Node(cfg)
    node.run()
    assert dummy_val == node.storage.get(cfg.name)


def tast_avaliable_tasks():
    assert type(task.tast_avaliable_tasks()) == list[str]
