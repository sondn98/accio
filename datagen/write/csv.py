from typing import Literal, Optional
from datagen.write.models import FileWriterConfig
from datagen.write.writer import BaseWriter, FileFormat, WriterFactory


class CSVWriterConfig(FileWriterConfig):
    type: Literal["csv"]
    header: bool = True
    delimiter: str = ","
    escape_char: str = "\\"
    quote_char: Optional[str] = None
    charset: Optional[str] = None


class CSVWriter(BaseWriter, FileFormat):
    def __init__(self, config: CSVWriterConfig):
        pass

    def write(self, row, **kwargs):
        pass

    def close(self):
        pass

    def path(self) -> str:
        pass

    def prepare_write(self, **kwargs) -> WriterFactory:
        pass

    def extension(self) -> str:
        pass

    def support_dtype(self, dtype: str) -> bool:
        pass
