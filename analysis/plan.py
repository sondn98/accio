from typing import Any, Callable, Dict, List, Set

from antlr4 import (BailErrorStrategy, CommonTokenStream, InputStream,
                    ParseTreeWalker)
from networkx import DiGraph, topological_sort
from pydantic import BaseModel

from analysis.listener import CoreListener
from gen.ConditionLexer import ConditionLexer
from gen.ConditionParser import ConditionParser
from models.config import Column, Condition, GeneratorConfig


class GenContext(BaseModel):
    deps: Set[str]
    generator_config: GeneratorConfig
    evaluator: Callable


def parse_condition(condition: Condition) -> GenContext:
    input_stream = InputStream(condition.predicate)
    lexer = ConditionLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = ConditionParser(stream)
    parser.errorHandler = BailErrorStrategy()
    tree = parser.condition()
    if parser.getNumberOfSyntaxErrors() > 0:
        raise Exception(f"Syntax errors: {condition.predicate}")
    else:
        ltn = CoreListener()
        walker = ParseTreeWalker()
        walker.walk(ltn, tree)

        if ltn and ltn.model:
            return GenContext(deps=ltn.deps, evaluator=ltn.model, generator_config=condition.spec)
        else:
            raise Exception(f"Unable to parse condition: {condition.predicate}")


def parse_node(column: Column) -> List[GenContext]:
    conditions = column.conditions
    return [parse_condition(cond) for cond in conditions] if conditions else []


class BaseFieldGraph:
    def __init__(self, dataset_name: str, columns: List[Column]):
        # Build dependency graph
        self._g = DiGraph()
        self._data = {}
        for index, column in enumerate(columns):
            node_id = f"{dataset_name}.{column.name}"
            contexts = parse_node(column)
            deps = set().union(*[ctx.deps for ctx in contexts])
            node_data = dict(contexts=contexts, deps=deps, index=index)
            self._g.add_node(node_id)
            self._data[node_id] = node_data
            for dep in node_data["deps"]:
                if "." not in dep:
                    dep = f"{dataset_name}.{dep}"
                self._g.add_edge(dep, node_id)

    def node_data(self, node_id: str) -> Dict[str, Any]:
        return self._data[node_id]

    def topo(self) -> List[str]:
        return list(topological_sort(self._g))
