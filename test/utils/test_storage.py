from omegaconf import OmegaConf

from scidag.utils.storage import Storage


def test_storage():
    cfg = OmegaConf.create({"name": "test", "dependencies": {}})
    storage = Storage(cfg)
    storage.put("this")
    storage.get("results")
