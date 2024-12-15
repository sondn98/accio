from enum import Enum
from typing import Annotated, Optional, Union
from pydantic import BaseModel, model_validator
from abc import ABC

from utils.assertions import assert_not_null


class WriterType(str, Enum):
    CSV = "csv"
    JDBC = "jdbc"


class JDBCWriterConfig(BaseModel):
    type: WriterType = WriterType.JDBC
    dbtype: str
    host: Optional[bool] = None
    port: Optional[str] = None
    jdbc_url: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    dn_name: str
    schema_name: Optional[str] = None
    table: str

    @model_validator(mode="after")
    def validate_params(self):
        if not self.jdbc_url:
            assert_not_null(self.host, self.port, self.username, self.password)


class FileWriterConfig(BaseModel, ABC):
    output_folder: str
    max_records_per_file: Optional[int] = None
    max_file_size_in_kb: Optional[int] = None
    filename_prefix: Optional[str] = None


class CSVWriterConfig(FileWriterConfig):
    type: WriterType = WriterType.CSV
    header: bool = True
    delimiter: str = ","
    escape_char: str = "\\"
    quote_char: Optional[str] = None
    charset: Optional[str] = None


WriterConfig = Annotated[Union[JDBCWriterConfig, CSVWriterConfig], "type"]
