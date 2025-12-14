from analysis.functions import FUNCTIONS
from gen.ConditionParserListener import ConditionParserListener
from gen.ConditionParser import ConditionParser
from utils.structures import Stack
from utils.log import get_logger
from typing import Any, Callable, List, Set


logger = get_logger(__file__)


class Node:

    def __init__(self):
        self._compiled_children: List[Any] = []

    @property
    def compiled(self):
        return self._compiled_children

    def update_parsed_child(self, parsed: Any):
        self._compiled_children.append(parsed)


class CoreListener(ConditionParserListener):
    def __init__(self):
        self.stack = Stack[Node]()
        self.evaluator: Callable
        self.dependent_nodes: Set[str] = set()

    def __put_onto_stack(self):
        node = Node()
        self.stack.push(node)
        logger.debug(f"____ Stack size: {len(self.stack)}")

    def _update_parent(self, x: Callable):
        if self.stack.empty():
            self.evaluator = x
        else:
            parent = self.stack.pop()
            parent.update_parsed_child(x)
            self.stack.push(parent)

    def __pop_from_stack(self) -> Node:
        top = self.stack.pop()
        logger.debug(f"____ Stack size: {len(self.stack)}")
        return top

    @property
    def model(self) -> Callable:
        return self.evaluator

    @property
    def deps(self) -> Set[str]:
        return self.dependent_nodes

    def enterCondition(self, ctx: ConditionParser.ConditionContext):
        logger.debug(f"Start analyzing condition... {ctx.getText()}")
        self.__put_onto_stack()

    def exitCondition(self, ctx: ConditionParser.ConditionContext):
        ctx.removeLastChild()
        logger.debug(f"Finish analyzing condition {ctx.getText()}")
        node = self.__pop_from_stack()
        parsed = node.compiled
        self._update_parent(lambda **kwargs: parsed[0](**kwargs))

    def enterBoolean_expression(self, ctx: ConditionParser.Boolean_expressionContext):
        logger.debug(f"Enter boolean expression {ctx.getText()}")
        for i in range(ctx.getChildCount()):
            logger.debug(f"==> Child {i}: {ctx.getChild(i).getText()}")
        self.__put_onto_stack()

    def exitBoolean_expression(self, ctx: ConditionParser.Boolean_expressionContext):
        logger.debug(f"Exit boolean expression {ctx.getText()}")
        node = self.__pop_from_stack()
        parsed = node.compiled
        if ctx.AND():
            logger.debug(f"====> boolean_expression case: boolean_expression AND boolean_expression")
            self._update_parent(lambda **kwargs: parsed[0](**kwargs) and parsed[1](**kwargs))
        elif ctx.OR():
            logger.debug(f"====> boolean_expression case: boolean_expression OR boolean_expression")
            self._update_parent(lambda **kwargs: parsed[0](**kwargs) or parsed[1](**kwargs))
        else:
            logger.debug(f"====> boolean_expression case: NOT* (LP boolean_expression RP | pred)")
            self._update_parent(lambda **kwargs: not parsed[0](**kwargs) if ctx.NOT() else parsed[0](**kwargs))

    def enterPred(self, ctx: ConditionParser.PredContext):
        logger.debug(f"Enter predicate {ctx.getText()}")
        for i in range(ctx.getChildCount()):
            logger.debug(f"==> Child {i}: {ctx.getChild(i).getText()}")
        self.__put_onto_stack()

    def exitPred(self, ctx: ConditionParser.PredContext):
        logger.debug(f"Exit predicate {ctx.getText()}")
        node = self.__pop_from_stack()
        parsed = node.compiled
        if ctx.IS() and ctx.NULL_():
            logger.debug(f"====> pred case: expression IS NOT? NULL_")
            self._update_parent(
                lambda **kwargs: parsed[0](**kwargs) is not None if ctx.NOT() else parsed[0](**kwargs) is None
            )
        elif ctx.LIKE():
            logger.debug(f"====> pred case: expression IS NOT? NULL_")
            import re

            self._update_parent(
                lambda **kwargs: (
                    not bool(re.compile(parsed[1](**kwargs)).fullmatch(parsed[0](**kwargs)))
                    if ctx.NOT()
                    else bool(re.compile(parsed[1](**kwargs)).fullmatch(parsed[0](**kwargs)))
                )
            )
        elif ctx.BETWEEN():
            logger.debug(f"====> pred case: expression IS NOT? NULL_")
            self._update_parent(
                lambda **kwargs: (
                    not parsed[1](**kwargs) < parsed[0](**kwargs) < parsed[2](**kwargs)
                    if ctx.NOT()
                    else parsed[1](**kwargs) < parsed[0](**kwargs) < parsed[2](**kwargs)
                )
            )
        elif ctx.IN():
            logger.debug(f"====> pred case: expression IS NOT? NULL_")
            self._update_parent(
                lambda **kwargs: (
                    not parsed[0](**kwargs) in parsed[1](**kwargs)
                    if ctx.NOT()
                    else parsed[0](**kwargs) in parsed[1](**kwargs)
                )
            )
        else:
            self._update_parent(lambda **kwargs: parsed[1](parsed[0](**kwargs), parsed[2](**kwargs)))

    def enterComparison_operator(self, ctx: ConditionParser.Comparison_operatorContext):
        logger.debug(f"Enter comparison operator {ctx.getText()}")
        self.__put_onto_stack()

    def exitComparison_operator(self, ctx: ConditionParser.Comparison_operatorContext):
        logger.debug(f"Exit comparison operator {ctx.getText()}")
        self.__pop_from_stack()
        op = ctx.getChild(0).getText()
        if op == "<":
            self._update_parent(lambda left, right: left < right)
        elif op == "=":
            self._update_parent(lambda left, right: left == right)
        elif op == ">":
            self._update_parent(lambda left, right: left > right)
        elif op == "<=":
            self._update_parent(lambda left, right: left <= right)
        elif op == ">=":
            self._update_parent(lambda left, right: left >= right)
        elif op == "<>" or op == "!=":
            self._update_parent(lambda left, right: left != right)
        else:
            raise Exception(f'Unrecognized comparison operator "{op}"')

    def enterExpression(self, ctx: ConditionParser.ExpressionContext):
        logger.debug(f"Enter expression {ctx.getText()}")
        for i in range(ctx.getChildCount()):
            logger.debug(f"==> Child {i}: {ctx.getChild(i).getText()}")
        self.__put_onto_stack()

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
            self._update_parent(lambda **kwargs: parsed[0](**kwargs))
        elif ctx.id_() and ctx.expression_list_():
            func = parsed[0]()
            self._update_parent(lambda **kwargs: func(*parsed[1](**kwargs)))
        elif ctx.getChildCount() == 2:
            sign = ctx.getChild(0).getText()
            self._update_parent(lambda **kwargs: -parsed[1](**kwargs) if sign == "-" else parsed[1](**kwargs))
        elif ctx.getChildCount() == 3 and ctx.getChild(1).getText() in ["*", "/", "%"]:
            sign = ctx.getChild(1).getText()
            self._update_parent(
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
            self._update_parent(
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
        self.__put_onto_stack()

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

        self._update_parent(__case_expr)

    def enterWhen_expression(self, ctx: ConditionParser.When_expressionContext):
        logger.debug(f"Enter when expression {ctx.getText()}")
        for i in range(ctx.getChildCount()):
            logger.debug(f"==> Child {i}: {ctx.getChild(i).getText()}")
        self.__put_onto_stack()

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

        self._update_parent(__when_expr)

    def enterPrimitive_expression(self, ctx: ConditionParser.Primitive_expressionContext):
        logger.debug(f"Enter primitive expression {ctx.getText()}")
        for i in range(ctx.getChildCount()):
            logger.debug(f"==> Child {i}: {ctx.getChild(i).getText()}")
        self.__put_onto_stack()

    def exitPrimitive_expression(self, ctx: ConditionParser.Primitive_expressionContext):
        logger.debug(f"Exit primitive expression {ctx.getText()}")
        node = self.__pop_from_stack()
        parsed = node.compiled
        self._update_parent(lambda **kwargs: parsed[0](**kwargs))

    def enterLiteral(self, ctx: ConditionParser.LiteralContext):
        logger.debug(f"Enter literal {ctx.getText()}")
        self.__put_onto_stack()

    def exitLiteral(self, ctx: ConditionParser.LiteralContext):
        logger.debug(f"Exit literal {ctx.getText()}")
        node = self.__pop_from_stack()
        parsed = node.compiled
        if ctx.NULL_():
            self._update_parent(lambda **kwargs: None)
        else:
            self._update_parent(lambda **kwargs: parsed[0](**kwargs))

    def enterNumber(self, ctx: ConditionParser.NumberContext):
        logger.debug(f"Enter number {ctx.getText()}")
        self.__put_onto_stack()

    def exitNumber(self, ctx: ConditionParser.NumberContext):
        logger.debug(f"Exit number {ctx.getText()}")
        node = self.__pop_from_stack()
        parsed = node.compiled
        if ctx.REAL_LITERAL() or ctx.FLOAT_LITERAL():
            self._update_parent(lambda **kwargs: float(ctx.getChild(0).getText()))
        else:
            self._update_parent(lambda **kwargs: int(parsed[0](**kwargs)))

    def enterTrue_false(self, ctx: ConditionParser.True_falseContext):
        logger.debug(f"Enter true/false {ctx.getText()}")
        self.__put_onto_stack()

    def exitTrue_false(self, ctx: ConditionParser.True_falseContext):
        logger.debug(f"Exit true/false {ctx.getText()}")
        self.__pop_from_stack()
        val = ctx.getChild(0).getText()
        self._update_parent(lambda **kwargs: True if val.upper() == "TRUE" else False)

    def enterExpression_list_(self, ctx: ConditionParser.Expression_list_Context):
        logger.debug(f"Enter expression list {ctx.getText()}")
        self.__put_onto_stack()

    def exitExpression_list_(self, ctx: ConditionParser.Expression_list_Context):
        logger.debug(f"Exit expression list {ctx.getText()}")
        node = self.__pop_from_stack()
        parsed = list(filter(lambda x: x is not None, node.compiled))
        self._update_parent(lambda **kwargs: [expr(**kwargs) for expr in parsed])

    def enterData_type(self, ctx: ConditionParser.Data_typeContext):
        logger.debug(f"Enter data type {ctx.getText()}")
        self.__put_onto_stack()

    def exitData_type(self, ctx: ConditionParser.Data_typeContext):
        logger.debug(f"Exit data type {ctx.getText()}")
        node = self.__pop_from_stack()
        parsed = node.compiled
        self._update_parent(lambda **kwargs: parsed[0](**kwargs))

    def enterPrimitive_type(self, ctx: ConditionParser.Primitive_typeContext):
        logger.debug(f"Enter primitive type {ctx.getText()}")
        self.__put_onto_stack()

    def exitPrimitive_type(self, ctx: ConditionParser.Primitive_typeContext):
        logger.debug(f"Exit primitive type {ctx.getText()}")
        node = self.__pop_from_stack()
        parsed = node.compiled
        from analysis.functions import DTYPE_FUNCTION_REGISTRY

        dtype_name = parsed[0].lower()
        self._update_parent(DTYPE_FUNCTION_REGISTRY[dtype_name])

    def enterPrecision(self, ctx: ConditionParser.PrecisionContext):
        logger.debug(f"Enter precision {ctx.getText()}")
        self.__put_onto_stack()

    def exitPrecision(self, ctx: ConditionParser.PrecisionContext):
        logger.debug(f"Exit precision {ctx.getText()}")
        node = self.__pop_from_stack()
        parsed = node.compiled
        self._update_parent(lambda **kwargs: parsed[0](**kwargs))

    def enterScale(self, ctx: ConditionParser.ScaleContext):
        logger.debug(f"Enter scale {ctx.getText()}")
        self.__put_onto_stack()

    def exitScale(self, ctx: ConditionParser.ScaleContext):
        logger.debug(f"Exit scale {ctx.getText()}")
        node = self.__pop_from_stack()
        parsed = node.compiled
        self._update_parent(lambda **kwargs: parsed[0](**kwargs))

    def enterString(self, ctx: ConditionParser.StringContext):
        logger.debug(f"Enter string {ctx.getText()}")
        self.__put_onto_stack()

    def exitString(self, ctx: ConditionParser.StringContext):
        logger.debug(f"exit string {ctx.getText()}")
        self.__pop_from_stack()
        self._update_parent(lambda **kwargs: ctx.getChild(0).getText()[1:-1])

    def enterInt_number(self, ctx: ConditionParser.Int_numberContext):
        logger.debug(f"Enter int number {ctx.getText()}")
        self.__put_onto_stack()

    def exitInt_number(self, ctx: ConditionParser.Int_numberContext):
        logger.debug(f"Exit int number {ctx.getText()}")
        self.__pop_from_stack()
        self._update_parent(lambda **kwargs: int(ctx.getChild(0).getText()))

    def enterId_(self, ctx: ConditionParser.Id_Context):
        logger.debug(f"Enter Id_ {ctx.getText()}")
        self.__put_onto_stack()

    def exitId_(self, ctx: ConditionParser.Id_Context):
        id_ = ctx.getText()
        logger.debug(f"Exit Id_ {id_}")
        self.__pop_from_stack()
        self._update_parent(lambda **kwargs: kwargs[id_] if id_ in kwargs else FUNCTIONS[id_])
        self.dependent_nodes.add(id_)
