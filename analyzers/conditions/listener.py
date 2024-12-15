from gen.ConditionParserListener import ConditionParserListener
from gen.ConditionParser import ConditionParser
from analyzers.conditions.functions import FUNCTIONS
from utils.lists import coalesce_idx
from collections import deque
from utils.log import get_logger
from typing import Any, Callable, List, Set


logger = get_logger(__file__)


class ParseNode:

    def __init__(self, depth: int, child_count: int):
        self.__depth: int = depth
        self.__compiled_children: List[Any] = [None] * child_count

    @property
    def depth(self):
        return self.__depth

    @property
    def compiled(self):
        return self.__compiled_children

    def update_parsed_child(self, parsed: Any):
        update_idx = coalesce_idx(self.__compiled_children)
        self.__compiled_children[update_idx] = parsed


class ParseStack:
    def __init__(self):
        self.__stack = deque()

    def __len__(self):
        return len(self.__stack)

    def push(self, x: ParseNode):
        self.__stack.append(x)

    def pop(self) -> ParseNode:
        return self.__stack.pop()

    def peak(self) -> ParseNode:
        return self.__stack[-1]

    def empty(self) -> bool:
        return not self.__stack


class CoreConditionListener(ConditionParserListener):
    def __init__(self):
        self._parse_stack = ParseStack()
        self.__model: Callable
        self.__deps: Set[str] = set()

    def __put_onto_stack(self, children_count):
        current_depth = len(self._parse_stack)
        node = ParseNode(current_depth + 1, children_count)
        self._parse_stack.push(node)
        logger.debug(f"____ Stack size: {len(self._parse_stack)}")

    def __update_parent(self, x: Callable):
        if self._parse_stack.empty():
            self.__model = x
        else:
            parent = self._parse_stack.pop()
            parent.update_parsed_child(x)
            self._parse_stack.push(parent)

    def __pop_from_stack(self) -> ParseNode:
        top = self._parse_stack.pop()
        logger.debug(f"____ Stack size: {len(self._parse_stack)}")
        return top

    def __add_dep(self, d):
        self.__deps.add(d)

    @property
    def model(self) -> Callable:
        return self.__model

    @property
    def deps(self) -> Set[str]:
        return self.__deps

    def enterCondition(self, ctx: ConditionParser.ConditionContext):
        logger.debug(f"Start analyzing condition... {ctx.getText()}")
        self.__put_onto_stack(ctx.getChildCount())

    def exitCondition(self, ctx: ConditionParser.ConditionContext):
        ctx.removeLastChild()
        logger.debug(f"Finish analyzing condition {ctx.getText()}")
        node = self.__pop_from_stack()
        parsed = node.compiled
        self.__update_parent(lambda **kwargs: parsed[0](**kwargs))

    def enterBoolean_expression(self, ctx: ConditionParser.Boolean_expressionContext):
        logger.debug(f"Enter boolean expression {ctx.getText()}")
        for i in range(ctx.getChildCount()):
            logger.debug(f"==> Child {i}: {ctx.getChild(i).getText()}")
        self.__put_onto_stack(ctx.getChildCount())

    def exitBoolean_expression(self, ctx: ConditionParser.Boolean_expressionContext):
        logger.debug(f"Exit boolean expression {ctx.getText()}")
        node = self.__pop_from_stack()
        parsed = node.compiled
        if ctx.AND():
            logger.debug(f"====> boolean_expression case: boolean_expression AND boolean_expression")
            self.__update_parent(lambda **kwargs: parsed[0](**kwargs) and parsed[1](**kwargs))
        elif ctx.OR():
            logger.debug(f"====> boolean_expression case: boolean_expression OR boolean_expression")
            self.__update_parent(lambda **kwargs: parsed[0](**kwargs) or parsed[1](**kwargs))
        else:
            logger.debug(f"====> boolean_expression case: NOT* (LP boolean_expression RP | pred)")
            self.__update_parent(lambda **kwargs: not parsed[0](**kwargs) if ctx.NOT() else parsed[0](**kwargs))

    def enterPred(self, ctx: ConditionParser.PredContext):
        logger.debug(f"Enter predicate {ctx.getText()}")
        for i in range(ctx.getChildCount()):
            logger.debug(f"==> Child {i}: {ctx.getChild(i).getText()}")
        self.__put_onto_stack(ctx.getChildCount())

    def exitPred(self, ctx: ConditionParser.PredContext):
        logger.debug(f"Exit predicate {ctx.getText()}")
        node = self.__pop_from_stack()
        parsed = node.compiled
        if ctx.IS() and ctx.NULL_():
            logger.debug(f"====> pred case: expression IS NOT? NULL_")
            self.__update_parent(
                lambda **kwargs: parsed[0](**kwargs) is not None if ctx.NOT() else parsed[0](**kwargs) is None
            )
        elif ctx.LIKE():
            logger.debug(f"====> pred case: expression IS NOT? NULL_")
            import re

            self.__update_parent(
                lambda **kwargs: (
                    not bool(re.compile(parsed[1](**kwargs)).fullmatch(parsed[0](**kwargs)))
                    if ctx.NOT()
                    else bool(re.compile(parsed[1](**kwargs)).fullmatch(parsed[0](**kwargs)))
                )
            )
        elif ctx.BETWEEN():
            logger.debug(f"====> pred case: expression IS NOT? NULL_")
            self.__update_parent(
                lambda **kwargs: (
                    not parsed[1](**kwargs) < parsed[0](**kwargs) < parsed[2](**kwargs)
                    if ctx.NOT()
                    else parsed[1](**kwargs) < parsed[0](**kwargs) < parsed[2](**kwargs)
                )
            )
        elif ctx.IN():
            logger.debug(f"====> pred case: expression IS NOT? NULL_")
            self.__update_parent(
                lambda **kwargs: (
                    not parsed[0](**kwargs) in parsed[1](**kwargs)
                    if ctx.NOT()
                    else parsed[0](**kwargs) in parsed[1](**kwargs)
                )
            )
        else:
            self.__update_parent(lambda **kwargs: parsed[1](parsed[0](**kwargs), parsed[2](**kwargs)))

    def enterComparison_operator(self, ctx: ConditionParser.Comparison_operatorContext):
        logger.debug(f"Enter comparison operator {ctx.getText()}")
        self.__put_onto_stack(ctx.getChildCount())

    def exitComparison_operator(self, ctx: ConditionParser.Comparison_operatorContext):
        logger.debug(f"Exit comparison operator {ctx.getText()}")
        self.__pop_from_stack()
        op = ctx.getChild(0).getText()
        if op == "<":
            self.__update_parent(lambda left, right: left < right)
        elif op == "=":
            self.__update_parent(lambda left, right: left == right)
        elif op == ">":
            self.__update_parent(lambda left, right: left > right)
        elif op == "<=":
            self.__update_parent(lambda left, right: left <= right)
        elif op == ">=":
            self.__update_parent(lambda left, right: left >= right)
        elif op == "<>" or op == "!=":
            self.__update_parent(lambda left, right: left != right)
        else:
            raise Exception(f'Unrecognized comparison operator "{op}"')

    def enterExpression(self, ctx: ConditionParser.ExpressionContext):
        logger.debug(f"Enter expression {ctx.getText()}")
        for i in range(ctx.getChildCount()):
            logger.debug(f"==> Child {i}: {ctx.getChild(i).getText()}")
        self.__put_onto_stack(ctx.getChildCount())

    def exitExpression(self, ctx: ConditionParser.ExpressionContext):
        logger.debug(f"Exit expression {ctx.getText()}")
        node = self.__pop_from_stack()
        parsed = node.compiled
        if (
            ctx.primitive_expression()
            or ctx.LP()
            and ctx.RP()
            and ctx.expression()
            and not ctx.CAST()
            or ctx.case_expression()
            or ctx.when_expression()
        ):
            self.__update_parent(lambda **kwargs: parsed[0](**kwargs))
        elif ctx.func():
            self.__update_parent(lambda **kwargs: parsed[0](*parsed[1](**kwargs)))
        elif ctx.getChildCount() == 2:
            sign = ctx.getChild(0).getText()
            self.__update_parent(lambda **kwargs: -parsed[1](**kwargs) if sign == "-" else parsed[1](**kwargs))
        elif ctx.getChildCount() == 3 and ctx.getChild(1).getText() in ["*", "/", "%"]:
            sign = ctx.getChild(1).getText()
            self.__update_parent(
                lambda **kwargs: (
                    parsed[0](**kwargs) * parsed[1](**kwargs)
                    if sign == "*"
                    else (
                        parsed[0](**kwargs) / parsed[1](**kwargs)
                        if sign == "/"
                        else parsed[0](**kwargs) % parsed[1](**kwargs)
                    )
                )
            )
        elif ctx.getChildCount() == 3 and ctx.getChild(1).getText() in ["+", "-"]:
            sign = ctx.getChild(1).getText()
            self.__update_parent(
                lambda **kwargs: (
                    parsed[0](**kwargs) + parsed[1](**kwargs)
                    if sign == "+"
                    else parsed[0](**kwargs) - parsed[1](**kwargs)
                )
            )
        elif ctx.CAST():
            raise NotImplementedError("Expression cast has not yet supported")
        else:
            raise ValueError(f"Unrecognized expression {ctx.getText()}")

    def enterCase_expression(self, ctx: ConditionParser.Case_expressionContext):
        logger.debug(f"Enter case expression {ctx.getText()}")
        for i in range(ctx.getChildCount()):
            logger.debug(f"==> Child {i}: {ctx.getChild(i).getText()}")
        self.__put_onto_stack(ctx.getChildCount())

    def exitCase_expression(self, ctx: ConditionParser.Case_expressionContext):
        logger.debug(f"Exit case expression {ctx.getText()}")
        node = self.__pop_from_stack()
        parsed = node.compiled

        def __case_expr(**kwargs):
            expected = parsed[0](**kwargs)
            final = parsed[-1](**kwargs) if ctx.ELSE() else None
            for i in range(1, len(parsed), 2):
                val_check = parsed[i](**kwargs)
                if expected == val_check:
                    return parsed[i + 1](**kwargs)

            return final

        self.__update_parent(__case_expr)

    def enterWhen_expression(self, ctx: ConditionParser.When_expressionContext):
        logger.debug(f"Enter when expression {ctx.getText()}")
        for i in range(ctx.getChildCount()):
            logger.debug(f"==> Child {i}: {ctx.getChild(i).getText()}")
        self.__put_onto_stack(ctx.getChildCount())

    def exitWhen_expression(self, ctx: ConditionParser.When_expressionContext):
        logger.debug(f"Exit when expression {ctx.getText()}")
        node = self.__pop_from_stack()
        parsed = node.compiled

        def __when_expr(**kwargs):
            final = parsed[-1](**kwargs) if ctx.ELSE() else None
            for i in range(0, len(parsed), 2):
                if parsed[i](**kwargs):
                    return parsed[i + 1](**kwargs)

            return final

        self.__update_parent(__when_expr)

    def enterPrimitive_expression(self, ctx: ConditionParser.Primitive_expressionContext):
        logger.debug(f"Enter primitive expression {ctx.getText()}")
        for i in range(ctx.getChildCount()):
            logger.debug(f"==> Child {i}: {ctx.getChild(i).getText()}")
        self.__put_onto_stack(ctx.getChildCount())

    def exitPrimitive_expression(self, ctx: ConditionParser.Primitive_expressionContext):
        logger.debug(f"Exit primitive expression {ctx.getText()}")
        node = self.__pop_from_stack()
        parsed = node.compiled
        self.__update_parent(lambda **kwargs: parsed[0](**kwargs))

    def enterLiteral(self, ctx: ConditionParser.LiteralContext):
        logger.debug(f"Enter literal {ctx.getText()}")
        self.__put_onto_stack(ctx.getChildCount())

    def exitLiteral(self, ctx: ConditionParser.LiteralContext):
        logger.debug(f"Exit literal {ctx.getText()}")
        node = self.__pop_from_stack()
        parsed = node.compiled
        if ctx.NULL_():
            self.__update_parent(lambda **kwargs: None)
        else:
            self.__update_parent(lambda **kwargs: parsed[0](**kwargs))

    def enterNumber(self, ctx: ConditionParser.NumberContext):
        logger.debug(f"Enter number {ctx.getText()}")
        self.__put_onto_stack(ctx.getChildCount())

    def exitNumber(self, ctx: ConditionParser.NumberContext):
        logger.debug(f"Exit number {ctx.getText()}")
        node = self.__pop_from_stack()
        parsed = node.compiled
        if ctx.REAL_LITERAL() or ctx.FLOAT_LITERAL():
            self.__update_parent(lambda **kwargs: float(ctx.getChild(0).getText()))
        else:
            self.__update_parent(lambda **kwargs: int(parsed[0](**kwargs)))

    def enterTrue_false(self, ctx: ConditionParser.True_falseContext):
        logger.debug(f"Enter true/false {ctx.getText()}")
        self.__put_onto_stack(ctx.getChildCount())

    def exitTrue_false(self, ctx: ConditionParser.True_falseContext):
        logger.debug(f"Exit true/false {ctx.getText()}")
        self.__pop_from_stack()
        val = ctx.getChild(0).getText()
        self.__update_parent(lambda **kwargs: True if val.upper() == "TRUE" else False)

    def enterExpression_list_(self, ctx: ConditionParser.Expression_list_Context):
        logger.debug(f"Enter expression list {ctx.getText()}")
        self.__put_onto_stack(ctx.getChildCount())

    def exitExpression_list_(self, ctx: ConditionParser.Expression_list_Context):
        logger.debug(f"Exit expression list {ctx.getText()}")
        node = self.__pop_from_stack()
        parsed = list(filter(lambda x: x is not None, node.compiled))
        self.__update_parent(lambda **kwargs: [expr(**kwargs) for expr in parsed])

    def enterData_type(self, ctx: ConditionParser.Data_typeContext):
        logger.debug(f"Enter data type {ctx.getText()}")
        self.__put_onto_stack(ctx.getChildCount())

    def exitData_type(self, ctx: ConditionParser.Data_typeContext):
        logger.debug(f"Exit data type {ctx.getText()}")
        node = self.__pop_from_stack()
        parsed = node.compiled
        self.__update_parent(lambda **kwargs: parsed[0](**kwargs))

    def enterPrimitive_type(self, ctx: ConditionParser.Primitive_typeContext):
        logger.debug(f"Enter primitive type {ctx.getText()}")
        self.__put_onto_stack(ctx.getChildCount())

    def exitPrimitive_type(self, ctx: ConditionParser.Primitive_typeContext):
        logger.debug(f"Exit primitive type {ctx.getText()}")
        node = self.__pop_from_stack()
        parsed = node.compiled
        from analyzers.conditions.functions import DTYPE_FUNCTION_REGISTRY

        dtype_name = parsed[0].lower()
        self.__update_parent(DTYPE_FUNCTION_REGISTRY[dtype_name])

    def enterPrecision(self, ctx: ConditionParser.PrecisionContext):
        logger.debug(f"Enter precision {ctx.getText()}")
        self.__put_onto_stack(ctx.getChildCount())

    def exitPrecision(self, ctx: ConditionParser.PrecisionContext):
        logger.debug(f"Exit precision {ctx.getText()}")
        node = self.__pop_from_stack()
        parsed = node.compiled
        self.__update_parent(lambda **kwargs: parsed[0](**kwargs))

    def enterScale(self, ctx: ConditionParser.ScaleContext):
        logger.debug(f"Enter scale {ctx.getText()}")
        self.__put_onto_stack(ctx.getChildCount())

    def exitScale(self, ctx: ConditionParser.ScaleContext):
        logger.debug(f"Exit scale {ctx.getText()}")
        node = self.__pop_from_stack()
        parsed = node.compiled
        self.__update_parent(lambda **kwargs: parsed[0](**kwargs))

    def enterString(self, ctx: ConditionParser.StringContext):
        logger.debug(f"Enter string {ctx.getText()}")
        self.__put_onto_stack(ctx.getChildCount())

    def exitString(self, ctx: ConditionParser.StringContext):
        logger.debug(f"exit string {ctx.getText()}")
        self.__pop_from_stack()
        self.__update_parent(lambda **kwargs: ctx.getChild(0).getText()[1:-1])

    def enterInt_number(self, ctx: ConditionParser.Int_numberContext):
        logger.debug(f"Enter int number {ctx.getText()}")
        self.__put_onto_stack(ctx.getChildCount())

    def exitInt_number(self, ctx: ConditionParser.Int_numberContext):
        logger.debug(f"Exit int number {ctx.getText()}")
        self.__pop_from_stack()
        self.__update_parent(lambda **kwargs: int(ctx.getChild(0).getText()))

    def enterFunc(self, ctx: ConditionParser.FuncContext):
        logger.debug(f"Enter Id_ {ctx.getText()}")
        self.__put_onto_stack(ctx.getChildCount())

    def exitFunc(self, ctx: ConditionParser.FuncContext):
        func_name = ctx.getText()
        logger.debug(f"Exit func {func_name}")
        self.__pop_from_stack()
        if func_name not in FUNCTIONS:
            raise ValueError(f"Unrecognized function {func_name}")
        self.__update_parent(FUNCTIONS[func_name])

    def enterId_(self, ctx: ConditionParser.Id_Context):
        logger.debug(f"Enter Id_ {ctx.getText()}")
        self.__put_onto_stack(ctx.getChildCount())

    def exitId_(self, ctx: ConditionParser.Id_Context):
        id_ = ctx.getText()
        logger.debug(f"Exit Id_ {id_}")
        self.__pop_from_stack()
        self.__update_parent(lambda **kwargs: kwargs[id_])
        self.__add_dep(id_)
