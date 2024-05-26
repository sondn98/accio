from models.configuration import Configuration
import yaml


def read_config(path: str) -> Configuration:
    with open(path, "r") as f:
        try:
            raw_cf = yaml.safe_load(f)
            return Configuration.model_validate(raw_cf)
        except Exception as e:
            raise Exception(f"Can not load yaml config file at path {path}", e)
