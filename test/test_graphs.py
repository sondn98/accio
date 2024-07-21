from files.reader import read_config
from analyzers.graph.builder import field_graph
from analyzers.graph.travel import bfs_from_sources


def test_build_graph():
    config_path = "test/resources/dataset_1.yaml"
    config = read_config(config_path)

    fields = config.datasets["dataset"].fields
    G = field_graph("dataset", fields)
    visited = bfs_from_sources(G)
    actual_visited = [
        "dataset.field_2",
        "dataset.field_6",
        "dataset.field_4",
        "dataset.field_5",
        "dataset.field_1",
        "dataset.field_3",
    ]

    assert len(visited) == len(actual_visited)
