import abc

__all__ = ["BaseElement"]


class BaseElement(abc.ABC):
    @abc.abstractmethod
    async def run(self):
        pass
