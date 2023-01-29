import abc


class Runnable(abc.ABC):
    @abc.abstractmethod
    def run(self) -> None:
        pass
