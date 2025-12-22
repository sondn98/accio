from analysis.plan import BaseFieldGraph
from models.config import read_config
from utils.assertions import assert_list_eq


def test_build_graph():
    config_path = "test/resources/dataset_1.yaml"
    config = read_config(config_path)

    ds_0 = config.datasets[0]
    graph = BaseFieldGraph(ds_0.name, ds_0.columns)
    topo = graph.topo()
    actual_visited = [
        "ds1.field_2",
        "ds1.field_4",
        "ds1.field_6",
        "ds1.field_5",
        "ds1.field_3",
        "ds1.field_1",
    ]

    assert_list_eq(actual_visited, topo)
