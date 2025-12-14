from typing import Annotated, Literal, Optional, Union
from pydantic import BaseModel


class CSVSerde(BaseModel):
    name: Literal["csv"]
    header: Optional[bool] = True
    delimiter: Optional[str] = ","
    escape_char: Optional[str] = "\\"
    quote_char: Optional[str] = None
    charset: Optional[str] = None


class FileWriterConfig(BaseModel):
    type: Literal["file"]
    output_folder: str
    max_records_per_file: Optional[int] = None
    max_file_size_in_kb: Optional[int] = None
    filename_prefix: Optional[str] = None
    serde: Annotated[Union[CSVSerde], "name"]
