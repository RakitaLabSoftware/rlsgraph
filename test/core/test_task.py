from omegaconf import DictConfig, OmegaConf

from scidag.core.task import Task


def test_task_run():
    cfg: DictConfig = OmegaConf.load(path)
    dummy_val = "dummy"
    task = Task(cfg)
    task.run()
    assert dummy_val == task.storage.get(cfg.name)


def tast_avaliable_tasks():
    assert type(task.tast_avaliable_tasks()) == list[str]
