import hydra_zen as hz

from scidag.utils.configurable import make_config


def func(a: int, b: int, mode: str = "sum"):
    match mode:
        case "sum":
            return a + b
        case "diff":
            return a - b
        case _:
            TypeError()


def test_configurable():
    cfg = make_config(func)
    assert func == hz.instantiate(cfg)
