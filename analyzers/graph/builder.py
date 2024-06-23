from networkx import DiGraph
from typing import Dict
from analyzers.conditions import parse
from models.condition import FieldsEvaluator
from models.config import Dataset


def build_fields_condition(datasets: Dict[str, Dataset]) -> FieldsEvaluator:
    for d_name, d_spect in datasets.items():
        fields = d_spect.fields
        for f_name, f_spec in fields.items():
            conditions = f_spec.conditions
            if conditions:
                for cond in conditions:
                    evaluator = parse(cond.predicate)


def build_graph(conditions: FieldsEvaluator) -> DiGraph:
    pass
