from configuration.provider import read_config


def test_load_configuration():
    config_path = "test/resources/dataset_1.yaml"
    config = read_config(config_path)

    ds = config.datasets[0]
    assert ds.size == 100
    assert ds.name == "ds1"
    assert len(ds.output) == 1
    assert len(ds.columns) == 6

    assert config.outputs[0].type == "csv"
