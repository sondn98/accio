from configuration.provider import read_config


def test_load_configuration():
    config_path = "test/resources/dataset_1.yaml"
    config = read_config(config_path)

    assert config.datasets["dataset"].size == 100
    assert config.datasets["dataset"].alias == "dataframe"
    assert len(config.datasets["dataset"].output) == 1
    assert len(config.datasets["dataset"].fields) == 6

    assert config.outputs["csv_output"].type == "csv"
