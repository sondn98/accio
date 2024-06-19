/*
AWS Athena grammar.
The MIT License (MIT).

Copyright (c) 2023, Michał Lorek.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
*/

// $antlr-format alignTrailingComments true, columnLimit 150, maxEmptyLinesToKeep 1, reflowComments false, useTab false
// $antlr-format allowShortRulesOnASingleLine true, allowShortBlocksOnASingleLine true, minEmptyLines 0, alignSemicolons ownLine
// $antlr-format alignColons trailing, singleLineOverrulesHangingColon true, alignLexerCommands true, alignLabels true, alignTrailers true

lexer grammar ConditionLexer;

options {
    caseInsensitive = true;
}

AND             : 'AND';
ARRAY           : 'ARRAY';
AS              : 'AS';
BETWEEN         : 'BETWEEN';
BIGINT          : 'BIGINT';
BINARY          : 'BINARY';
BOOLEAN         : 'BOOLEAN';
CASE            : 'CASE';
CAST            : 'CAST';
CHAR            : 'CHAR';
COMMENT         : 'COMMENT';
DATABASES       : 'DATABASES';
DATE            : 'DATE';
DECIMAL         : 'DECIMAL';
DOUBLE          : 'DOUBLE';
ELSE            : 'ELSE';
END             : 'END';
FLOAT           : 'FLOAT';
FALSE           : 'FALSE';
IN              : 'IN';
INT             : 'INT';
INTEGER         : 'INTEGER';
NOT             : 'NOT';
NULL_           : 'NULL';
MAP             : 'MAP';
LIKE            : 'LIKE';
IS              : 'IS';
OR              : 'OR';
TIMESTAMP       : 'TIMESTAMP';
STRING          : 'STRING';
SMALLINT        : 'SMALLINT';
TINYINT         : 'TINYINT';
STRUCT          : 'STRUCT';
THEN            : 'THEN';
TRUE            : 'TRUE';
VARCHAR         : 'VARCHAR';
WHEN            : 'WHEN';

EQ     : '=';
SEMI   : ';';
LP     : '(';
RP     : ')';
DOT    : '.';
COMMA  : ',';
LT     : '<';
GT     : '>';
LE     : '<=';
GE     : '>=';
NE     : '<>';
BOX    : '!=';
COLON  : ':';
QM     : '?';
STAR   : '*';
PLUS   : '+';
MINUS  : '-';
DIVIDE : '/';
MODULE : '%';

fragment Letter: 'A' ..'Z';

fragment DIGIT: '0' ..'9';

fragment DEC_DOT_DEC: (DIGIT+ '.' DIGIT+ | DIGIT+ '.' | '.' DIGIT+);

fragment BLANK: (' ' | '\r' | '\n' | '\t' );

fragment NAME: Letter (Letter | DIGIT | '_')*;

COLUMN_NAME: NAME '.' NAME;

IDENTIFIER: NAME;

SQ_STRING_LITERAL: '\'' ( ~('\'' | '\\') | ('\\' .))* '\'';

INTEGRAL_LITERAL: DIGIT+;

FLOAT_LITERAL: DEC_DOT_DEC;

REAL_LITERAL: (INTEGRAL_LITERAL | DEC_DOT_DEC) ('E' [+-]? DIGIT+);

WS : BLANK+ -> skip;
