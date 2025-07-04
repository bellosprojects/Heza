from parser import Parser
from lexer import Lexer
from interprete import Heza
import json, sys

#Codigo fuente

if len(sys.argv) > 1:

    path = sys.argv[1]

    code = open(path).read()

    lexer = Lexer(code)
    tokens = lexer.tokenize()
    #print(tokens)

    parser = Parser(tokens)
    ast = parser.parse_program()
    #print(json.dumps(ast,indent=2))

    heza = Heza(ast)
    heza.run()
    #heza.debug()

#https://drive.google.com/file/d/1ysd1atyM8JuLFFLFQTjSbbFA8ecSvCq3/view?usp=sharing