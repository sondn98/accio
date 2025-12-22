import json

from datagen.storage.engine import Storage

mock_data = [
    json.dumps({"field1": "data11", "field2": 121}).encode("utf-8"),
    json.dumps({"field1": "data12", "field2": 122}).encode("utf-8"),
    json.dumps({"field1": "data13", "field2": 123}).encode("utf-8"),
    json.dumps({"field1": "data14", "field2": 124}).encode("utf-8"),
    json.dumps({"field1": "data15", "field2": 125}).encode("utf-8"),
    json.dumps({"field1": "data16", "field2": 126}).encode("utf-8"),
    json.dumps({"field1": "data17", "field2": 127}).encode("utf-8"),
    json.dumps({"field1": "data18", "field2": 128}).encode("utf-8"),
    json.dumps({"field1": "data19", "field2": 129}).encode("utf-8"),
]


def test_insert(sql_cli):
    sql_cli.create_table(Storage)
    for item in mock_data:
        sql_cli.insert(Storage(dataset="test", data=item))
    cnt = sql_cli.count(Storage, Storage.dataset == "test")
    assert cnt == 9
