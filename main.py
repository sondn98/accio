from collections.abc import Callable
from typing import Any, Union

from pydantic import (AliasChoices, AmqpDsn, BaseModel, Field, ImportString,
                      PostgresDsn, RedisDsn)
from pydantic_settings import BaseSettings, SettingsConfigDict

from models.config import Configuration


class AppSettings(BaseSettings):
    config_file: str
    config: Configuration

    model_config = SettingsConfigDict(cli_parse_args=True)


if __name__ == "__main__":
    pass
