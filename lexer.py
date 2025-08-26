from tokens import tokens
import re

class Lexer:
    def __init__(self, code):
        self.code = code
        self.pos = 0
        self.tokens_result = []

    def tokenize(self):
        while self.pos < len(self.code):
            for token, patron in tokens:
                regex = re.compile(patron)
                match = regex.match(self.code, self.pos)
                if match:
                    if token not in ['IGNORAR', 'COMENTARIO']:
                        valor = match.group()
                        if token == 'NUMBER':
                            valor = int(float(valor)) if float(valor) % 1 == 0.0 else float(valor)
                        elif token == 'STR' or token == 'EXPRESION':
                            valor = valor[1:-1]

                        self.tokens_result.append((token, valor))
                    self.pos = match.end()
                    break
            else:
                print(f"Error token desconocido {self.code[self.pos]}")
                exit()

        return self.tokens_result