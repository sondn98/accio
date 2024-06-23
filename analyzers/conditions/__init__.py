from analyzers.conditions.listener import CoreConditionListener
from gen.ConditionParser import ConditionParser
from gen.ConditionLexer import ConditionLexer
from antlr4 import InputStream, CommonTokenStream, ParseTreeWalker, BailErrorStrategy
from models.condition import CondMatcher, CondNode
from models.config import Condition, BaseField


def parse(cond: Condition) -> CondMatcher:
    input_stream = InputStream(cond.predicate)
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
        return CondMatcher(deps=listener_.deps, evaluator=listener_.model, generator_params=cond.params)
    else:
        raise Exception(f"Unable to parse condition: {cond.predicate}")
