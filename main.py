from collections.abc import Callable
from typing import Any

from pydantic import (
    AliasChoices,
    AmqpDsn,
    BaseModel,
    Field,
    ImportString,
    PostgresDsn,
    RedisDsn,
)

from pydantic_settings import BaseSettings, SettingsConfigDict


class SubModel(BaseModel):
    foo: str = "bar"
    apple: int = 1


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="my_prefix_")
    lol: str = "ttt"
    auth_key: str = Field(validation_alias="my_auth_key")

    api_key: str = Field(alias="my_api_key")

    redis_dsn: RedisDsn = Field(
        "redis://user:pass@localhost:6379/1",
        validation_alias=AliasChoices("service_redis_dsn", "redis_url"),
    )
    pg_dsn: PostgresDsn = "postgres://user:pass@localhost:5432/foobar"
    amqp_dsn: AmqpDsn = "amqp://user:pass@localhost:5672/"

    special_function: ImportString[Callable[[Any], Any]] = "math.cos"

    # to override domains:
    # export my_prefix_domains='["foo.com", "bar.com"]'
    domains: set[str] = set()

    # to override more_settings:
    # export my_prefix_more_settings='{"foo": "x", "apple": 1}'
    more_settings: SubModel = SubModel()


print(
    Settings(my_auth_key="abc", my_api_key="xyz", service_redis_dsn="redis://user:pass@localhost:6379/2").model_dump()
)
