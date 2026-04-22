from typing import Annotated, Literal, Optional, Union

from pydantic import BaseModel, DirectoryPath


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
    output_folder: DirectoryPath
    filename_prefix: Optional[str] = None
    serde: Annotated[Union[CSVSerde], "format"]
