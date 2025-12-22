from typing import Annotated, Literal, Optional, Union, Any

from pydantic import BaseModel
from pydantic.main import IncEx


class CSVSerde(BaseModel):
    format: Literal["csv"]
    header: Optional[bool] = True
    encoding: Optional[str] = "utf-8"
    delimiter: Optional[str] = ","
    escapechar: Optional[str] = "\\"
    doublequote: Optional[bool] = None
    skipinitialspace: Optional[bool] = None
    lineterminator: Optional[str] = None
    quotechar: Optional[str] = None
    quoting: Optional[str] = None


class FileWriterConfig(BaseModel):
    name: str
    type: Literal["file"]
    output_folder: str
    filename_prefix: Optional[str] = None
    serde: Annotated[Union[CSVSerde], "format"]
