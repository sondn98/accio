from files.reader import read_config


# TODO: Complete the test
def test_load_configuration():
    config_path = "test/resources/dataset_1.yaml"
    config = read_config(config_path)

    assert config.datasets["dataset"].population == 100
