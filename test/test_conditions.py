from analyzers.conditions import parse
import csv


def test_listener():
    resource_folder = "test/resources/conditions"
    data_file = f"{resource_folder}/data-test.csv"
    cond_file = f"{resource_folder}/conditions.txt"

    data = []
    with open(data_file, "r") as f:
        rdr = csv.DictReader(f, delimiter=",", quotechar='"')
        for line in rdr:
            d_data = dict(line)
            test_case = dict(
                idx=int(d_data["cond_idx"]),
                actual=True if d_data["actual"] == "true" else False if d_data["actual"] == "false" else None,
                params={
                    "ds.a": int(d_data["ds.a"]) if d_data["ds.a"] else None,
                    "ds.b": int(d_data["ds.b"]) if d_data["ds.b"] else None,
                    "ds.c": int(d_data["ds.c"]) if d_data["ds.c"] else None,
                    "ds.d": str(d_data["ds.d"]) if d_data["ds.d"] else None,
                    "ds.e": str(d_data["ds.e"]) if d_data["ds.e"] else None,
                    "ds.f": str(d_data["ds.f"]) if d_data["ds.f"] else None,
                },
            )
            data.append(test_case)

    with open(cond_file, "r") as f:
        for idx, raw_cond in enumerate(f):
            cond = parse(raw_cond)
            evaluator = cond.evaluate
            for tc in data:
                if tc["idx"] == idx:
                    assert evaluator(**tc["params"]) == tc["actual"]
