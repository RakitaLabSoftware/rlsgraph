from typing import Self

from scidag.utils.configurable import NodeConfig

from .base import BaseNode


class EndNode(BaseNode):
    @classmethod
    def from_config(cls, cfg: NodeConfig) -> Self:
        return super().from_config(cfg)

    def to_config(self) -> NodeConfig:
        return super().to_config()

    async def run(self):
        inputs = await self.get_inputs()
        outputs = self.content(**inputs)
