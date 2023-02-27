from typing import Self

from scidag.utils.configurable import NodeConfig

from .base import BaseNode


class StartNode(BaseNode):
    async def run(self):
        outputs = self.content()
        assert outputs is not None, f"{self.name}"
        self.storage.store(self.name, outputs)

    @classmethod
    def from_config(cls, cfg: NodeConfig) -> Self:
        return super().from_config(cfg)

    def to_config(self) -> NodeConfig:
        return super().to_config()
