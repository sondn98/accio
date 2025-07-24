from abc import ABC, abstractmethod


class Storage(ABC):
    @abstractmethod
    def store(self, item):
        pass

    @abstractmethod
    def flush(self):
        pass


class MemoryAndDisk(Storage):
    pass


class MemoryOnly(Storage):
    pass
