from parser import Parser
from lexer import Lexer
from interprete import Heza
import json, sys

#Codigo fuente

if len(sys.argv) > 1:

    path = sys.argv[1]

    code = open(path, encoding="UTF-8").read()

    lexer = Lexer(code)
    tokens = lexer.tokenize()
    #print(tokens)

    parser = Parser(tokens)
    ast = parser.parse_program()
    #print(json.dumps(ast,indent=2))

    heza = Heza(ast)
    heza.run()
    #heza.debug()

#https://github.com/bellosprojects/Heza/blob/main/HezaSetup.exe