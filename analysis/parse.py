from antlr4 import BailErrorStrategy, CommonTokenStream, InputStream

from analysis.ast import ASTBuilder
from gen.SqlExprLexer import SqlExprLexer
from gen.SqlExprParser import SqlExprParser
from utils.log import get_logger

logger = get_logger(__name__)


def parse(evaluation: str):
    input_stream = InputStream(evaluation)
    lexer = SqlExprLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = SqlExprParser(stream)
    parser.errorHandler = BailErrorStrategy()
    tree = parser.evaluation()
    if parser.getNumberOfSyntaxErrors() > 0:
        # if False: # Uncomment this for debugging only
        raise Exception(f"Syntax errors: {evaluation}")
    else:
        ast = ASTBuilder()
        root = ast.visit(tree)
        predecessors = ast.predecessors
        return root, predecessors
