parser grammar ConditionParser;

options {
    tokenVocab = ConditionLexer;
}

condition
    : boolean_expression
    ;

boolean_expression
    : boolean_expression AND boolean_expression
    | boolean_expression OR boolean_expression
    | NOT* (LP boolean_expression RP | pred)
    ;

pred
    : expression comparison_operator expression
    | expression IS NOT? NULL_
    | id_ NOT? LIKE string
    | expression NOT? BETWEEN expression AND expression
    | expression NOT? IN LP expression_list_ RP
    ;

comparison_operator
    : LT
    | EQ
    | GT
    | LE
    | GE
    | NE
    | BOX
    ;

expression
    : primitive_expression
    | LP expression RP
    | func LP expression_list_ RP
    | case_expression
    | when_expression
    | op = (PLUS | MINUS) expression
    | expression op = (STAR | DIVIDE | MODULE) expression
    | expression op = (PLUS | MINUS) expression
    | CAST LP expression AS data_type RP
    ;

case_expression
    : CASE expression (WHEN expression THEN expression)+ (ELSE expression)? END
    ;

when_expression
    : CASE (WHEN boolean_expression THEN expression)+ (ELSE expression)? END
    ;

primitive_expression
    : literal
    | id_
    ;

literal
    : number
    | string
    | true_false
    | NULL_
    ;

number
    : int_number
    | REAL_LITERAL
    | FLOAT_LITERAL
    ;

true_false
    : TRUE
    | FALSE
    ;

expression_list_
    : expression (COMMA expression)*
    ;

data_type
    : primitive_type
    ;

primitive_type
    : BOOLEAN
    | TINYINT
    | SMALLINT
    | INT
    | INTEGER
    | BIGINT
    | DOUBLE
    | FLOAT
    | DECIMAL LP precision COMMA scale RP
    | (CHAR | VARCHAR) LP int_number RP
    | STRING
    | BINARY
    | DATE
    | TIMESTAMP
    ;

precision
    : int_number
    ;

scale
    : int_number
    ;

string
    : SQ_STRING_LITERAL
    ;

int_number
    : INTEGRAL_LITERAL
    ;

func
    : IDENTIFIER
    ;

id_
    : COLUMN_NAME
    ;
