from models.write.files import CSVSerde
from datagen.write.writer import BaseWriter, FileFormat, WriterFactory


class CSVWriter(BaseWriter, FileFormat):
    def __init__(self, config: CSVSerde):
        pass

    def write(self, row, **kwargs):
        pass

    def close(self):
        pass

    def path(self) -> str:
        pass

    def prepare_write(self, **kwargs) -> WriterFactory:
        pass

    @property
    def extension(self) -> str:
        return "csv"

    def support_dtype(self, dtype: str) -> bool:
        pass
