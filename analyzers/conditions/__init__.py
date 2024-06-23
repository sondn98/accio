from analyzers.conditions.listener import CoreConditionListener
from gen.ConditionParser import ConditionParser
from gen.ConditionLexer import ConditionLexer
from antlr4 import InputStream, CommonTokenStream, ParseTreeWalker, BailErrorStrategy
from models.condition import Evaluator


def parse(cond: str) -> Evaluator:
    input_stream = InputStream(cond)
    lexer = ConditionLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = ConditionParser(stream)
    parser.errorHandler = BailErrorStrategy()
    tree = parser.condition()
    if parser.getNumberOfSyntaxErrors() > 0:
        raise Exception("Syntax errors")
    else:
        listener_ = CoreConditionListener()
        walker = ParseTreeWalker()
        walker.walk(listener_, tree)

    if listener_ and listener_.model:
        return Evaluator(deps=listener_.deps, evaluate=listener_.model)
    else:
        raise Exception(f"Unable to create condition from: {cond}")
