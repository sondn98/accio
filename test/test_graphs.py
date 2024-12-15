from configuration.provider import read_config
from analyzers.plan import field_graph
from analyzers.travel import bfs_from_sources


def test_build_graph():
    config_path = "test/resources/dataset_1.yaml"
    config = read_config(config_path)

    fields = config.datasets["dataset"].fields
    print(fields)
    G = field_graph(fields)
    visited = bfs_from_sources(G)
    actual_visited = [
        "dataset.field_2",
        "dataset.field_6",
        "dataset.field_4",
        "dataset.field_5",
        "dataset.field_1",
        "dataset.field_3",
    ]
    print(G.nodes)
    print(visited)

    assert len(visited) == len(actual_visited)
