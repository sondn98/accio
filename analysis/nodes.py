from __future__ import annotations

import re
from collections import namedtuple
from typing import Any, Callable, List, Type

from analysis.functions import FUNCTIONS


class TreeNode:
    def __init__(self, evaluator: Callable[..., Any], children: List[Type[TreeNode]]):
        self._evaluator = evaluator
        self._children = children

    def evaluate(self, **values) -> Any:
        evaluated_children = [c.evaluate(**values) for c in self._children]
        return self._evaluator(*evaluated_children)


class UnaryNode(TreeNode):
    def __init__(self, child):
        super().__init__(lambda v: v, [child])


class LeafNode(TreeNode):
    def __init__(self, eval_func):
        super().__init__(eval_func, [])


class Condition(TreeNode):
    @classmethod
    def boolean_expression(cls, expr):
        return cls(evaluator=lambda e: bool(e), children=[expr])

    @classmethod
    def expression(cls, expr):
        return cls(evaluator=lambda e: e, children=[expr])


class BooleanExpr(TreeNode):
    @classmethod
    def and_expr(cls, left: Type[TreeNode], right: Type[TreeNode]):
        """
        Handle: boolean_expression AND boolean_expression
        :param left:
        :param right:
        :return:
        """
        return cls(evaluator=lambda first, second: first and second, children=[left, right])

    @classmethod
    def or_expr(cls, left, right):
        """
        Handle: boolean_expression OR boolean_expression
        :param left:
        :param right:
        :return:
        """
        return cls(evaluator=lambda first, second: first or second, children=[left, right])

    @classmethod
    def predicate(cls, expr, neg):
        """
        Handle: NOT* (LP boolean_expression RP | pred)
        :param expr:
        :param neg:
        :return:
        """
        return cls(evaluator=lambda e: not e if neg else e, children=[expr])


class Predicate(TreeNode):
    @classmethod
    def lt(cls, left, right):
        """
        Handle: expression > expression
        :param left:
        :param right:
        :return:
        """
        return cls(evaluator=lambda l, r: l and r and l < r, children=[left, right])

    @classmethod
    def le(cls, left, right):
        """
        Handle: expression > expression
        :param left:
        :param right:
        :return:
        """
        return cls(evaluator=lambda l, r: l <= r, children=[left, right])

    @classmethod
    def eq(cls, left, right):
        """
        Handle: expression > expression
        :param left:
        :param right:
        :return:
        """
        return cls(evaluator=lambda l, r: l == r, children=[left, right])

    @classmethod
    def gt(cls, left, right):
        """
        Handle: expression > expression
        :param left:
        :param right:
        :return:
        """
        return cls(evaluator=lambda l, r: l > r, children=[left, right])

    @classmethod
    def ge(cls, left, right):
        """
        Handle: expression > expression
        :param left:
        :param right:
        :return:
        """
        return cls(evaluator=lambda l, r: l >= r, children=[left, right])

    @classmethod
    def ne(cls, left, right):
        """
        Handle: expression > expression
        :param left:
        :param right:
        :return:
        """
        return cls(evaluator=lambda l, r: l != r, children=[left, right])

    @classmethod
    def null_check(cls, expr, neg):
        """
        Handle: expression IS NOT? NULL_
        :param expr:
        :return:
        """
        return cls(evaluator=lambda e: e is not None if neg else e is None, children=[expr])

    @classmethod
    def like(cls, id_, regex, neg):
        """
        Handle: id_ NOT? LIKE string
        :param id_:
        :return:
        """

        def match(s, r):
            pythonic_regex = re.escape(r).replace(r"%", ".*").replace(r"_", ".")
            normalized = "^" + pythonic_regex + "$"
            match_result = bool(re.fullmatch(normalized, s))
            return not match_result if neg else match_result

        return cls(evaluator=match, children=[id_, regex])

    @classmethod
    def between(cls, expr, left, right, neg):
        """
        Handle: expression NOT? BETWEEN expression AND expression
        :param expr:
        :param left:
        :param right:
        :return:
        """
        return cls(evaluator=lambda e, l, r: not (l <= e <= r) if neg else l <= e <= r, children=[expr, left, right])

    @classmethod
    def in_list(cls, expr, expr_list, neg):
        """
        Handle: expression NOT? IN LP expression_list_ RP
        :param expr:
        :param expr_list:
        :return:
        """
        return cls(evaluator=lambda e, lst: e not in lst if neg else e in lst, children=[expr, expr_list])


class Expression(TreeNode):
    @classmethod
    def primitive(cls, expr):
        """
        Handle: primitive_expression
        :param primitive:
        :return:
        """
        return cls(evaluator=lambda e: e, children=[expr])

    @classmethod
    def parenthesized_expr(cls, expr):
        """
        Handle: LP expression RP
        :param expr:
        :return:
        """
        return cls(evaluator=lambda e: e, children=[expr])

    @classmethod
    def function_call(cls, func, expr_list):
        """
        Handle: id_ LP expression_list_ RP
        :param func:
        :param expr_list:
        :return:
        """
        return cls(evaluator=lambda f, e_lst: f(*e_lst), children=[func, expr_list])

    @classmethod
    def case_expr(cls, case_expr):
        """
        Handle: case_expression
        :param case_expr:
        :return:
        """
        return cls(evaluator=lambda e: e, children=[case_expr])

    @classmethod
    def when_expr(cls, when_expr):
        """
        Handle: when_expression
        :param when_expr:
        :return:
        """
        return cls(evaluator=lambda e: e, children=[when_expr])

    @classmethod
    def expr_with_op(cls, expr, minus):
        """
        Handle: op = (PLUS | MINUS) expression
        :param op:
        :param expr:
        :return:
        """
        return cls(evaluator=lambda e: -e if minus else e, children=[expr])

    @classmethod
    def plus(cls, left, right):
        """

        :param left:
        :param right:
        :return:
        """
        return cls(evaluator=lambda l, r: l + r, children=[left, right])

    @classmethod
    def minus(cls, left, right):
        """

        :param left:
        :param right:
        :return:
        """
        return cls(evaluator=lambda l, r: l - r, children=[left, right])

    @classmethod
    def multiply(cls, left, right):
        """

        :param left:
        :param right:
        :return:
        """
        return cls(evaluator=lambda l, r: l * r, children=[left, right])

    @classmethod
    def divide(cls, left, right):
        """

        :param left:
        :param right:
        :return:
        """
        return cls(evaluator=lambda l, r: l / r, children=[left, right])

    @classmethod
    def mod(cls, left, right):
        """

        :param left:
        :param right:
        :return:
        """
        return cls(evaluator=lambda l, r: l % r, children=[left, right])

    @classmethod
    def cast(cls, expr, dtype):
        """
        Handle: CAST LP expression AS data_type RP
        :param expr:
        :param dtype:
        :return:
        """

        def _do_cast(val, tp):
            raise NotImplementedError("CAST has not yet been supported")

        return cls(evaluator=_do_cast, children=[expr, dtype])


class CaseExpression(TreeNode):
    WhenStmt = namedtuple("WhenStmt", ["value_expr", "result_expr"])

    def __init__(self, expr, default_result):
        def _do_match_cases(e, dft=None, *when_expr):
            print(when_expr)
            for v, r in when_expr:
                match = e == v if e else v
                if match:
                    return r
            return dft

        super().__init__(_do_match_cases, [expr, default_result])

    def with_when_stmt(self, value, result):
        self._children.extend([value, result])


class WhenExpression(CaseExpression):
    def __init__(self, default_result):
        super().__init__(None, default_result)


class Primitive(UnaryNode):
    pass


class Literal(UnaryNode):
    pass


class Number(UnaryNode):
    pass


class ExprList(TreeNode):
    @classmethod
    def expressions(cls, expr_lst):
        return cls(evaluator=lambda *x: x, children=expr_lst)


class DataType(TreeNode):
    @classmethod
    def primitive_type(cls, dtype):
        pass


class PrimitiveType(TreeNode):
    @classmethod
    def primitive(cls, dtype, **kwargs):
        pass


class Precision(UnaryNode):
    pass


class Scale(UnaryNode):
    pass


class String(LeafNode):
    pass


class IntNumber(LeafNode):
    pass


class Id(LeafNode):
    def __init__(self, name, must_be_field):
        super().__init__(None)
        self.name = name
        self.must_be_field = must_be_field

    @property
    def is_attribute(self):
        return self.must_be_field or self.name not in FUNCTIONS

    def evaluate(self, **values) -> Any:
        if not self.is_attribute:
            return FUNCTIONS[self.name]

        if self.name in values:
            return values[self.name]
        else:
            successors = list(filter(lambda x: x.endswith(f".{self.name}"), values.keys()))
            if not successors:
                raise SyntaxError("Unknown id %s", self.name)
            elif len(successors) > 1:
                raise RuntimeError("Attribute %s is ambiguous", self.name)
            key = successors[0]
            return values[key]
