from analysis.nodes import *
from gen.SqlExprParser import SqlExprParser
from gen.SqlExprParserVisitor import SqlExprParserVisitor
from utils.log import get_logger

logger = get_logger(__name__)


class ASTBuilder(SqlExprParserVisitor):
    def __init__(self):
        self._predecessors = set()

    @property
    def predecessors(self):
        return self._predecessors

    # Visit a parse tree produced by SqlExprParser#condition.
    def visitEvaluation(self, ctx: SqlExprParser.EvaluationContext):
        logger.debug("Visit Condition: %s", ctx.getText())
        if ctx.boolean_expression():
            boolean = self.visitBoolean_expression(ctx.boolean_expression())
            return Condition.boolean_expression(boolean)
        else:
            expr = self.visitExpression(ctx.expression())
            return Condition.expression(expr)

    # Visit a parse tree produced by SqlExprParser#boolean_expression.
    def visitBoolean_expression(self, ctx: SqlExprParser.Boolean_expressionContext):
        logger.debug("Visit Boolean Expression: %s", ctx.getText())
        if ctx.AND() or ctx.OR():
            left = self.visitBoolean_expression(ctx.boolean_expression(0))
            right = self.visitBoolean_expression(ctx.boolean_expression(1))
            return BooleanExpr.and_expr(left, right) if ctx.AND() else BooleanExpr.or_expr(left, right)
        else:
            expr = ctx.pred()
            if expr:
                return BooleanExpr.predicate(self.visitPred(expr), ctx.NOT())
            else:
                expr = self.visitBoolean_expression(ctx.boolean_expression(0))
                return BooleanExpr.predicate(expr, ctx.NOT())

    # Visit a parse tree produced by SqlExprParser#pred.
    def visitPred(self, ctx: SqlExprParser.PredContext):
        logger.debug("Visit Predicate: %s", ctx.getText())
        if ctx.comparison_operator():
            op = ctx.comparison_operator()
            left = self.visitExpression(ctx.expression(0))
            right = self.visitExpression(ctx.expression(1))
            if op.LT():
                return Predicate.lt(left, right)
            elif op.LE():
                return Predicate.le(left, right)
            elif op.EQ():
                return Predicate.eq(left, right)
            elif op.GT():
                return Predicate.gt(left, right)
            elif op.ge():
                return Predicate.ge(left, right)
            elif op.ne() or op.box():
                return Predicate.ne(left, right)
            else:
                raise SyntaxError("Unknown comparison operator")
        elif ctx.IS() and ctx.NULL_():
            expr = self.visitExpression(ctx.expression(0))
            return Predicate.null_check(expr, ctx.NOT())
        elif ctx.LIKE():
            id = self.visitId_(ctx.id_())
            regex = self.visitString(ctx.string())
            return Predicate.like(id, regex, ctx.NOT())
        elif ctx.BETWEEN():
            expr = self.visitExpression(ctx.expression(0))
            left = self.visitExpression(ctx.expression(1))
            right = self.visitExpression(ctx.expression(2))
            return Predicate.between(expr, left, right, ctx.NOT())
        elif ctx.IN():
            expr = self.visitExpression(ctx.expression(0))
            expr_list = self.visitExpression_list_(ctx.expression_list_())
            return Predicate.in_list(expr, expr_list, ctx.NOT())
        else:
            raise SyntaxError("Unknown predicate")

    # Visit a parse tree produced by SqlExprParser#expression.
    def visitExpression(self, ctx: SqlExprParser.ExpressionContext):
        logger.debug("Visit Expression: %s, %d", ctx.getText(), ctx.getChildCount())
        if ctx.primitive_expression():
            expr = self.visitPrimitive_expression(ctx.primitive_expression())
            return Expression.primitive(expr)
        elif ctx.case_expression():
            expr = self.visitCase_expression(ctx.case_expression())
            return Expression.case_expr(expr)
        elif ctx.when_expression():
            expr = self.visitCase_expression(ctx.when_expression())
            return Expression.when_expr(expr)
        elif ctx.id_() and ctx.expression_list_():
            id = self.visitId_(ctx.id_())
            expr_list = self.visitExpression_list_(ctx.expression_list_())
            return Expression.function_call(id, expr_list)
        elif ctx.LP() and ctx.RP() and ctx.getChildCount() == 3:
            expr = self.visitExpression(ctx.expression(0))
            return Expression.parenthesized_expr(expr)
        elif ((ctx.MINUS() or ctx.PLUS()) and ctx.getChildCount() == 2) or ctx.getChildCount() == 1:
            expr = self.visitExpression(ctx.expression(0))
            return Expression.expr_with_op(expr, ctx.MINUS())
        elif (ctx.PLUS() or ctx.MINUS() or ctx.DIVIDE() or ctx.STAR() or ctx.MODULE()) and ctx.getChildCount() == 3:
            left = self.visitExpression(ctx.expression(0))
            right = self.visitExpression(ctx.expression(1))
            if ctx.PLUS():
                return Expression.plus(left, right)
            elif ctx.MINUS():
                return Expression.minus(left, right)
            elif ctx.STAR():
                return Expression.multiply(left, right)
            elif ctx.DIVIDE():
                return Expression.divide(left, right)
            elif ctx.MODULE():
                return Expression.mod(left, right)
            else:
                raise SyntaxError("Unknown comparison operator")
        elif ctx.CAST():
            expr = self.visitExpression(ctx.expression(0))
            dtype = self.visitData_type(ctx.data_type())
            return Expression.cast(expr, dtype)
        else:
            raise SyntaxError("Unknown expression")

    # Visit a parse tree produced by SqlExprParser#case_expression.
    def visitCase_expression(self, ctx: SqlExprParser.Case_expressionContext):
        logger.debug("Visit Case Expression: %s", ctx.getText())
        all_expr = list(ctx.getChildren(lambda child: isinstance(child, SqlExprParser.ExpressionContext)))
        expr = self.visitExpression(all_expr[0])
        dft_expr = self.visitExpression(all_expr[-1]) if ctx.ELSE() else None
        expr_node = CaseExpression(expr, dft_expr)
        when_expr = list(zip(all_expr[1::2], all_expr[2::2]))
        for v, r in when_expr:
            expr_node.with_when_stmt(self.visitExpression(v), self.visitExpression(r))
        return expr_node

    # Visit a parse tree produced by SqlExprParser#when_expression.
    def visitWhen_expression(self, ctx: SqlExprParser.When_expressionContext):
        logger.debug("Visit When Expression: %s", ctx.getText())
        all_expr = list(ctx.getChildren(lambda child: isinstance(child, SqlExprParser.ExpressionContext)))
        dft_expr = self.visitExpression(all_expr[-1]) if ctx.ELSE() else None
        expr_node = WhenExpression(dft_expr)
        when_expr = list(zip(all_expr[::2], all_expr[1::2]))
        for v, r in when_expr:
            expr_node.with_when_stmt(self.visitExpression(v), self.visitExpression(r))

        return expr_node

    # Visit a parse tree produced by SqlExprParser#primitive_expression.
    def visitPrimitive_expression(self, ctx: SqlExprParser.Primitive_expressionContext):
        logger.debug("Visit Primitive Expression: %s", ctx.getText())
        return Primitive(self.visitChildren(ctx))

    # Visit a parse tree produced by SqlExprParser#literal.
    def visitLiteral(self, ctx: SqlExprParser.LiteralContext):
        logger.debug("Visit Literal: %s", ctx.getText())
        if ctx.NULL_():
            return LeafNode(lambda: None)
        return Literal(self.visitChildren(ctx))

    # Visit a parse tree produced by SqlExprParser#number.
    def visitNumber(self, ctx: SqlExprParser.NumberContext):
        logger.debug("Visit Number: %s", ctx.getText())
        if ctx.REAL_LITERAL() or ctx.FLOAT_LITERAL():
            return LeafNode(lambda x: float(x))
        return Number(self.visitInt_number(ctx.int_number()))

    # Visit a parse tree produced by SqlExprParser#true_false.
    def visitTrue_false(self, ctx: SqlExprParser.True_falseContext):
        logger.debug("Visit True/False: %s", ctx.getText())
        return LeafNode(lambda: True if ctx.TRUE() else False)

    # Visit a parse tree produced by SqlExprParser#expression_list_.
    def visitExpression_list_(self, ctx: SqlExprParser.Expression_list_Context):
        logger.debug("Visit Boolean Expression: %s", ctx.getText())

        all_expr = list(ctx.getChildren(lambda child: isinstance(child, SqlExprParser.ExpressionContext)))
        expr_nodes = [self.visitExpression(e) for e in all_expr]
        return ExprList.expressions(expr_nodes)

    # Visit a parse tree produced by SqlExprParser#data_type.
    def visitData_type(self, ctx: SqlExprParser.Data_typeContext):
        logger.debug("Visit Data Type: %s", ctx.getText())
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SqlExprParser#primitive_type.
    def visitPrimitive_type(self, ctx: SqlExprParser.Primitive_typeContext):
        logger.debug("Visit Primitive Type: %s", ctx.getText())
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SqlExprParser#precision.
    def visitPrecision(self, ctx: SqlExprParser.PrecisionContext):
        logger.debug("Visit Precision: %s", ctx.getText())
        int_number = self.visitInt_number(ctx.int_number())
        return Precision(int_number)

    # Visit a parse tree produced by SqlExprParser#scale.
    def visitScale(self, ctx: SqlExprParser.ScaleContext):
        logger.debug("Visit Scale: %s", ctx.getText())
        int_number = self.visitInt_number(ctx.int_number())
        return Scale(int_number)

    # Visit a parse tree produced by SqlExprParser#string.
    def visitString(self, ctx: SqlExprParser.StringContext):
        logger.debug("Visit String: %s", ctx.getText())
        return String(lambda: ctx.SQ_STRING_LITERAL().getText().strip("'"))

    # Visit a parse tree produced by SqlExprParser#int_number.
    def visitInt_number(self, ctx: SqlExprParser.Int_numberContext):
        logger.debug("Visit Int Number: %s", ctx.getText())
        return IntNumber(lambda: int(ctx.INTEGRAL_LITERAL().getText()))

    # Visit a parse tree produced by SqlExprParser#id_.
    def visitId_(self, ctx: SqlExprParser.Id_Context):
        logger.debug("Visit Id: %s", ctx.getText())
        must_be_field = True if ctx.DQ_STRING_LITERAL() else False
        id_name = ctx.DQ_STRING_LITERAL() or ctx.IDENTIFIER()
        id_node = Id(id_name.getText(), must_be_field)
        if id_node.is_attribute:
            self._predecessors.add(id_name.getText())

        return id_node
