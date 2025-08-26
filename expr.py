from lexer import Lexer
from parser import Parser

class Expresion():
    def __init__(self,expr):
        self.expr = expr

    def to_ast(self):
        tokens = Lexer(self.expr).tokenize()
        parsed = Parser(tokens, True).parse_program()
        return parsed
    
    def __str__(self):
        return self.expr