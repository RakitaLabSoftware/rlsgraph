from typing import Self

from scidag.utils.configurable import NodeConfig

from .base import BaseNode


class Node(BaseNode):
    """
    Base node Class
    """

    @classmethod
    def from_config(cls, cfg: NodeConfig) -> Self:
        return super().from_config(cfg)

    def to_config(self) -> NodeConfig:
        return super().to_config()

    async def run(self) -> None:
        try:
            inputs = await self.get_inputs()
            outputs = self.content(**inputs)
            self.storage.store(self.name, outputs)
        except Exception:
            print(f"failed in {self.name}")
            raise
