from abc import ABC, abstractmethod
from typing import Iterable, List, Protocol, Type, Union

from pydantic import BaseModel

from models.config import WriterConfig


class Writer(Protocol):
    def write(self, row: BaseModel, *args, **kwargs):
        """

        :param row:
        :param args:
        :param kwargs:
        :return:
        """
        ...


class BatchWriter(Protocol):
    def write_batch(self, rows: Iterable[BaseModel], *args, **kwargs):
        """

        :param rows:
        :param args:
        :param kwargs:
        :return:
        """
        ...


class AdaptiveWriter:
    def __init__(self, writer_impl: Union[Writer, BatchWriter]):
        self._writer_impl = writer_impl

    def write(self, row: BaseModel, *args, **kwargs):
        if hasattr(self._writer_impl, "write"):
            self._writer_impl.write(row, *args, **kwargs)
        else:
            self.write_batch([row], *args, **kwargs)

    def write_batch(self, rows: Iterable[BaseModel], *args, **kwargs):
        if hasattr(self._writer_impl, "write_batch"):
            self._writer_impl.write_batch(rows, *args, **kwargs)
        else:
            for row in rows:
                self.write(row, *args, **kwargs)


class FanoutWriter(AdaptiveWriter):
    def __init__(self, writer_impl: Union[Writer, BatchWriter], *writers_impl: Union[Writer, BatchWriter]):
        super().__init__(writer_impl)
        self.writer_impl = [writers_impl]

    def write(self, row: BaseModel, *args, **kwargs):
        if hasattr(self._writer_impl, "write"):
            self._writer_impl.write(row)
        else:
            self.write_batch([row])

    def write_batch(self, rows: Iterable[BaseModel], *args, **kwargs):
        if hasattr(self._writer_impl, "write_batch"):
            self._writer_impl.write_batch(rows)
        else:
            for row in rows:
                self.write(row)


def create_writer(output: WriterConfig):
    if output.type == "file":
        serde = output.serde
        if serde.format == "csv":
            from datagen.write.files.csv import CSVWriter

            return CSVWriter(output.output_folder, serde)
        else:
            raise NotImplemented(f"Unsupported file writer format {serde.format}")
    elif output.type == "jdbc":
        raise NotImplemented(f"Unsupported writer type {output.type}")
    else:
        raise NotImplemented(f"Unsupported writer type {output.type}")


class WriterFactory(ABC):
    @abstractmethod
    def new_instance(self, *args, **kwargs) -> Union[Writer, BatchWriter]:
        pass


class BaseWriterFactory(WriterFactory):
    def __init__(self, *outputs: WriterConfig):
        self._writer = {o.name: create_writer(o) for o in outputs}

    def new_instance(self, outputs: List[str], *args, **kwargs) -> Union[Writer, BatchWriter]:
        if len(outputs) > 1:
            _writers = [self._writer[o] for o in outputs]
            return FanoutWriter(*_writers)
        else:
            o = outputs[0]
            _writer = self._writer[o]
            return AdaptiveWriter(_writer)
