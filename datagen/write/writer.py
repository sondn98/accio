from abc import ABC, abstractmethod


class BaseWriter(ABC):
    @abstractmethod
    def write(self, row, **kwargs):
        pass

    @abstractmethod
    def close(self):
        pass

    @abstractmethod
    def path(self) -> str:
        pass


class WriterFactory(ABC):
    @abstractmethod
    def new_instance(self, **kwargs) -> BaseWriter:
        pass


class FileFormat(ABC):
    @abstractmethod
    def prepare_write(self, **kwargs) -> WriterFactory:
        pass

    @abstractmethod
    def extension(self) -> str:
        pass

    @abstractmethod
    def support_dtype(self, dtype: str) -> bool:
        pass
