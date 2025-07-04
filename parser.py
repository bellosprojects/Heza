from tokens import ExpresionValues

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current_token = tokens[0] if tokens else None

    def advance(self):
        self.pos += 1
        self.current_token = self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def Error(self, msg):
        print(msg)
        exit()

    def parse(self):
        return self.parse_program()
    
    def parse_program(self):
        program = []
        while self.current_token is not None:
            init = self.parse_init()
            program.append(init)

        return {"program": program}

    def parse_init(self,ret=False):
        if self.current_token[0] == 'DATA':
            return self.parse_data()
        elif self.current_token[0] in ['ID']:

            temp_pos = self.pos
            temp_token = self.tokens[temp_pos+1]
            name = self.current_token[1]
            if temp_token and temp_token[0] == 'OPENP':
                self.advance()
                self.advance()
                return self.parse_call(name)
            elif temp_token and temp_token[0] == 'PUNTO':
                id_ = self.current_token[1]
                self.advance()
                return self.parse_method(id_)

            return self.parse_reasignacion()
        elif self.current_token[0] == 'CLS':
            self.advance()
            return {
                    'type':'CLS'
                    }
        
        elif self.current_token[0] == 'BLOCK':
            return self.parse_block()
        elif self.current_token[0] == 'Q':
            return self.parse_condicional(ret)
        elif self.current_token[0] == 'LOOP':
            temp_pos = self.pos
            temp_token = self.current_token

            accion = 'None'
            while temp_token:
                if temp_token[0] == 'AS':
                    accion = 'for'
                    break
                elif temp_token[0] == 'Q':
                    accion = 'while'
                    break
                temp_pos+=1
                temp_token = self.tokens[temp_pos] if temp_pos<len(self.tokens) else None
            
            if accion == 'for':
                return self.parse_loop(ret)
            elif accion == 'while':
                return self.parse_while(ret)
            else:
                self.Error("Error en la sintaxis de la sentencia de loop")

        elif self.current_token[0] == 'OUT':
            return self.parse_out()
        elif self.current_token[0] == 'IN':
            return self.parse_in()
        elif self.current_token[0] == 'ARROW' and ret:
            return self.parse_arrow()
        elif self.current_token[0] == 'ENDNOW':
            return self.parse_endnow()

        else:
            self.Error(f"Error de sintaxis: {self.current_token[1]} inesperado")

    def parse_endnow(self):
        self.advance()
        if not self.current_token or self.current_token[0] != 'REFERENCE':
            self.Error("Error de sintaxis: Faltan argumentos para ENDNOW")
        self.advance()

        if not self.current_token or self.current_token[0] != 'ID':
            self.Error("Error de sintaxis: Faltan argumentos para ENDNOW")
        id_ = self.current_token[1]
        self.advance()

        return {'type':'endnow','alias':id_}

    def parse_method(self,id_):

        if not self.current_token or self.current_token[0] != 'PUNTO':
            self.Error("Error de sintaxis: PUNTO esperado")
        self.advance()

        if not self.current_token or self.current_token[0] != 'ID':
            self.Error("Error de sintaxis: identificador de metodo esperado")

        func = self.current_token[1]
        self.advance()

        if not self.current_token or self.current_token[0] != 'OPENP':
            self.Error("Error de sintaxis: abrir parentesis esperado")
        self.advance()

        if not self.current_token:
            self.Error("Error de sintaxis: argumentos de metodo esperados")

        args = []
        if self.current_token[0] != 'CLOSEP':
            while self.current_token[0] in ExpresionValues:
                args.append(self.parse_logico())

                if not self.current_token or self.current_token[0] != 'COMA':
                    break
                self.advance()

        if not self.current_token or self.current_token[0] != 'CLOSEP':
            self.Error("Error de sintaxis: cerrar parentesis esperado")

        self.advance()

        return {
            'type':'method',
            'id':{'type':'id','valor':id_},
            'function':func,
            'args':args
        }

    def parse_arrow(self):
        self.advance()
        values = []
        while self.current_token[0] in ExpresionValues:
            dato = self.parse_logico()
            values.append(dato)

            if not self.current_token or self.current_token[0] != 'COMA':
                break
            self.advance()

        return {'type':'return', 'values':values}

    def parse_block(self):
        self.advance()

        if not self.current_token or self.current_token[0] != 'ID':
            self.Error("Error de sintaxis: bloque sin identificador")
        name = self.current_token[1]
        self.advance()

        if not self.current_token or self.current_token[0] != 'OPENP':
            self.Error("Error de sintaxis: bloque sin paréntesis de apertura")
        self.advance()

        if not self.current_token:
            self.Error("Error de sintaxis: bloque sin contenido")

        args = []
        if self.current_token[0] != 'CLOSEP':
            while True:
                if self.current_token[0] != 'ID':
                    self.Error("Error de sintaxis: argumento no válido")
                args.append(self.current_token[1])
                self.advance()

                if self.current_token[0] != 'COMA':
                    break
                self.advance()

        if not self.current_token or self.current_token[0] != 'CLOSEP':
            self.Error("Error de sintaxis: bloque sin paréntesis de cierre")
        self.advance()

        body = []
        while self.current_token is not None:
            if self.current_token[0] == 'END':
                if self.pos+2 < len(self.tokens) and self.tokens[self.pos+2][1] == name:
                    break
            body.append(self.parse_init(True))

        if self.current_token is None or self.current_token[0]!='END':
            self.Error(f"Error de sintaxis: se esperaba end:{name}")

        self.advance()

        if self.current_token[0] != 'REFERENCE':
            self.Error(f"Error de sintaxis: se esperaba : despues de end")

        self.advance()

        if self.current_token[0] != 'ID' or self.current_token[1] != name:
            self.Error(f"Error de sintaxis: se esperaba el alias {name}")

        self.advance()

        return {
            'type': 'function',
            'name': name,
            'args': args,
            'body': body
        }


    def parse_while(self,ret):
        if self.current_token[0] != 'LOOP':
            self.Error(f"Error de sintaxis: se esperaba LOOP")
        self.advance()
        if self.current_token[0] != 'OPENP':
            self.Error(f"Error de sintaxis: se esperaba (")
        self.advance()

        condicion = self.parse_logico()

        if self.current_token[0] != 'CLOSEP':
            self.Error(f"Error de sintaxis: se esperaba )")
        self.advance()

        if self.current_token[0] != 'Q':
            self.Error(f"Error de sintaxis: se esperaba ?")
        self.advance()

        if self.current_token[0] != 'AS':
            self.Error(f"Error de sintaxis: se esperaba un apodo para loop")
        self.advance()

        if self.current_token[0] != 'ID':
            self.Error(f"Error de sintaxis: se esperaba un apodo para loop")
        alias = self.current_token[1]
        self.advance()

        body = []
        while self.current_token[0] is not None:
            if self.current_token[0] == 'END':
                if self.pos+2 < len(self.tokens) and self.tokens[self.pos+2][1] == alias:
                    break
            body.append(self.parse_init(ret))

        if self.current_token is None or self.current_token[0]!='END':
            self.Error(f"Error de sintaxis: se esperaba end:{alias}")

        self.advance()

        if self.current_token[0] != 'REFERENCE':
            self.Error(f"Error de sintaxis: se esperaba : despues de end")

        self.advance()

        if self.current_token[0] != 'ID' or self.current_token[1] != alias:
            self.Error(f"Error de sintaxis: se esperaba el alias {alias}")
        alias = self.current_token[1]
        self.advance()

        return {
            'type': 'while',
            'condition': condicion,
            'body': body,
            'alias': alias
            }

    def parse_loop(self,ret):
        if self.current_token[0] != 'LOOP':
            self.Error(f"Error de sintaxis: se esperaba LOOP")
        self.advance()
        if self.current_token[0] != 'OPENP':
            self.Error(f"Error de sintaxis: se esperaba (")
        self.advance()

        start = self.parse_logico()

        if self.current_token[0] != 'REFERENCE':
            self.Error(f"Error de sintaxis: se esperaba :")
        self.advance()

        end = self.parse_logico()

        if self.current_token[0] != 'REFERENCE':
                self.Error(f"Error de sintaxis: se esperaba :")
        self.advance()

        increment = self.parse_logico()

        if self.current_token[0] != 'CLOSEP':
            self.Error(f"Error de sintaxis: se esperaba )")
        self.advance()

        if self.current_token[0] != 'AS':
            self.Error(f"Error de sintaxis: se esperaba un apodo para loop")
        self.advance()

        if self.current_token[0] != 'ID':
            self.Error(f"Error de sintaxis: se esperaba un apodo para loop")
        alias = self.current_token[1]
        self.advance()

        body = []
        while self.current_token[0] is not None:
            if self.current_token[0] == 'END':
                if self.pos+2 < len(self.tokens) and self.tokens[self.pos+2][1] == alias:
                    break
            body.append(self.parse_init(ret))

        if self.current_token is None or self.current_token[0]!='END':
            self.Error(f"Error de sintaxis: se esperaba end:{alias}")

        self.advance()

        if self.current_token[0] != 'REFERENCE':
            self.Error(f"Error de sintaxis: se esperaba : despues de end")

        self.advance()

        if self.current_token[0] != 'ID' or self.current_token[1] != alias:
            self.Error(f"Error de sintaxis: se esperaba el alias {alias}")

        self.advance()

        return {'type':'loop',
                'alias':alias,
                'start':start,
                'end':end,
                'increment':increment,
                'body':body}

    def parse_condicional(self,ret):

        self.advance()

        condicion = self.parse_logico()

        if self.current_token[0] != 'Q':
            self.Error(f"Error de sintaxis: se esperaba el operador ?")
        self.advance()

        if self.current_token[0] != 'AS':
            self.Error(f"Error de sintaxis: se esperaba as despues del operador ?")
        self.advance()

        if self.current_token[0] != 'ID':
            self.Error(f"Error de sintaxis: se esperaba un identificador para el condicional")
        alias = self.current_token[1]
        self.advance()

        body = []
        while self.current_token is not None:
            if self.current_token[0] == 'END':
                if self.pos+2 < len(self.tokens) and self.tokens[self.pos+2][1] == alias:
                    break
            body.append(self.parse_init(ret))

        if self.current_token is None or self.current_token[0]!='END':
            self.Error(f"Error de sintaxis: se esperaba end:{alias}")

        self.advance()

        if self.current_token[0] != 'REFERENCE':
            self.Error(f"Error de sintaxis: se esperaba : despues de end")

        self.advance()

        if self.current_token[0] != 'ID' or self.current_token[1] != alias:
            self.Error(f"Error de sintaxis: se esperaba el alias {alias}")

        self.advance()

        return {'type': 'condicional', 'condicion': condicion, 'body': body}

    def parse_pipe(self):        
        pass

    def parse_in(self):

        if not self.current_token or self.current_token[0] != 'IN':
            self.Error("Error de sintaxis: se esperaba un operador de entrada")
        self.advance()

        if not self.current_token or self.current_token[0] != 'ARROW':
            self.Error("Error de sintaxis: se esperaba un operador de entrada")
        self.advance()

        if not self.current_token:
            self.Error("Error de sintaxis: se esperaba un valor")

        variables = []
        while self.current_token[0] == 'ID':
            var_name = self.current_token[1]
            variables.append(var_name)
            self.advance()

            if not self.current_token or self.current_token[0] != 'COMA':
                break
            self.advance()

        return {
                'type':'entrada',
                'variables':variables
                }


    def parse_out(self):
        
        if not self.current_token or self.current_token[0] != 'OUT':
            self.Error("Error de sintaxis: se esperaba un operador de salida")
        self.advance()

        if not self.current_token or self.current_token[0] != 'ARROW':
            self.Error("Error de sintaxis: se esperaba un operador de salida")
        self.advance()

        datos = []

        if not self.current_token:
            self.Error("Error de sintaxis: se esperaba un valor")

        while self.current_token[0] in ExpresionValues:
            dato = self.parse_logico()
            datos.append(dato)

            if not self.current_token or self.current_token[0] != 'COMA':
                break
            self.advance()

        return {
                'type':'salida',
                'datos':datos
                }

    def parse_reasignacion(self):

        variables = []
        while True:
            if self.current_token[0] != 'ID':
                self.Error("Error de sintaxis: se esperaba un Identificador")
            var_name = self.current_token[1]
            variables.append(var_name)
            self.advance()

            if self.current_token[0] != 'COMA':
                break
            self.advance()

        if not self.current_token or self.current_token[0] != 'ASIGNACION':
            self.Error("Error de sintaxis: se esperaba un signo de asignacion")

        self.advance()

        valores = []
        while True:
            valores.append(self.parse_logico())

            if not self.current_token or self.current_token[0] != 'COMA':
                break
            self.advance()

        if len(variables) != len(valores):
            self.Error("Error de sintaxis: la cantidad de variables no coincide con la cantidad de valores")

        return {
                'type':'reasignacion',
                'variables':variables,
                'valores':valores
                }

    def parse_data(self):
        self.advance()
        trace = False
        if self.current_token and self.current_token[0]=='TRACE':
            self.advance()
            trace=True
        
        variables = self.parse_list_declaration()

        return {
                'type':'data_declaration',
                'trace':trace,
                'variables':variables
                }
        
    def parse_list_declaration(self):
        variables = []
        while True:
            if not self.current_token or self.current_token[0] != 'ID':
                self.Error("Error de sintaxis: se esperaba un Identificador")

            var_name = self.current_token[1]
            self.advance()

            var = {
                    'name':var_name,
                    'value':None
                    }
        
            if self.current_token and self.current_token[0] == 'ASIGNACION':
                self.advance()
                var['value'] = self.parse_logico()

            variables.append(var)

            if not self.current_token or self.current_token[0] != 'COMA':
                break
            self.advance()
        return variables

    def parse_call(self,finc_name):
        args = []
        if self.current_token[0] != 'CLOSEP':
            while self.current_token[0] in ExpresionValues:
                dato = self.parse_logico()
                args.append(dato)

                if not self.current_token or self.current_token[0] != 'COMA':
                    break
                self.advance()

        if not self.current_token or self.current_token[0] != 'CLOSEP':
            self.Error("Error de sintaxis: se esperaba ) despues de los argumentos")
        self.advance()

        return {
            'type':'call',
            'name':finc_name,
            'args':args
        }


    def parse_term(self):
        if self.current_token is not None and self.current_token[0]=='NUMBER':
            valor = self.current_token[1]
            self.advance()
            return {
                    'type':'number',
                    'valor':valor
                    }
        elif self.current_token is not None and self.current_token[0]=='STR':
            valor = self.current_token[1]
            self.advance()
            return {
                    'type':'str',
                    'valor':valor
                    }
        elif self.current_token is not None and self.current_token[0]=='ID':
            nombre = self.current_token[1]
            self.advance()

            if self.current_token and self.current_token[0] == 'OPENP':
                self.advance()
                return self.parse_call(nombre)
            elif self.current_token and self.current_token[0] == 'PUNTO':
                return self.parse_method(nombre)
            else:
                return {
                        'type':'id',
                        'valor':nombre
                        }
        elif self.current_token is not None and self.current_token[0] in ['FALSE','TRUE']:
            valor = True if self.current_token[0] == 'TRUE' else False
            self.advance()
            return {
                    'type':'boolean',
                    'valor':valor
                    }
        elif self.current_token is not None and self.current_token[0] in ['LINE','TAB','ESP']:
            valor = " "
            if self.current_token[0] == 'LINE':
                valor = '\n'
            elif self.current_token[0] == 'TAB':
                valor = '\t'
            self.advance()
            return {
                    'type':'constant',
                    'valor':valor
                    }
        elif self.current_token is not None and self.current_token[0] == 'TRACE':
            self.advance()
            if not self.current_token or self.current_token[0] != 'REFERENCE':
                self.Error("Error sintactico: 'TRACE' sin referencia")
            self.advance()
            if not self.current_token or self.current_token[0] != 'ID':
                self.Error("Error sintactico: 'TRACE' sin identificador")
            nombre = self.current_token[1]
            self.advance()

            return {'type':'trace','valor':nombre}
        else:
            self.Error("Se esperaba una expresion")

    def parse_parentesis(self):
        if self.current_token is not None and self.current_token[0] == 'OPENP':
            self.advance()
            expr = self.parse_not()
            if self.current_token is not None and self.current_token[0] == 'CLOSEP':
                self.advance()
                return expr
            else:
                self.Error("Error de sintaxis: se esperaba un parentesis cerrado")
        else:
            return self.parse_term()
    
    
    def parse_pow(self):
        left = self.parse_parentesis()
        while self.current_token is not None and self.current_token[0] in ['POW']:
            op = self.current_token[0]
            self.advance()
            right = self.parse_parentesis()
            left = {
                    'type':'binary_operation',
                    'op':op,
                    'left':left,
                    'right':right
                    }
        return left
    
    def parse_multiplicacion(self):
        left = self.parse_pow()
        while self.current_token is not None and self.current_token[0] in ['MULTIPLICACION','DIVISION','MOD']:
            op = self.current_token[0]
            self.advance()
            right = self.parse_pow()
            left = {
                    'type':'binary_operation',
                    'op':op,
                    'left':left,
                    'right':right
                    }
        return left
        
    def parse_adicion(self):
        left = self.parse_multiplicacion()
        while self.current_token is not None and self.current_token[0] in ['SUMA','RESTA']:
            op = self.current_token[0]
            self.advance()
            right = self.parse_multiplicacion()
            left = {
                    'type':'binary_operation',
                    'op':op,
                    'left':left,
                    'right':right
                    }
        return left
    
    def parse_comparacion(self):
        left = self.parse_adicion()
        while self.current_token is not None and self.current_token[0] in ['COMPARACION','DISTINTO','MAYORE','MENORE','MAYOR','MENOR']:
            op = self.current_token[0]
            self.advance()
            right = self.parse_adicion()
            left = {
                    'type':'binary_operation',
                    'op':op,
                    'left':left,
                    'right':right
                    }
        return left
    
    def parse_not(self):
        if self.current_token is not None and self.current_token[0] in ['NOT','RESTA','SUMA']:
            op = self.current_token[0]
            self.advance()
            expr = self.parse_comparacion()
            return {
                    'type':'unary_operation',
                    'op':op,
                    'valor':expr
                    }
        else:
            return self.parse_comparacion()
        
    def parse_logico(self):
        left = self.parse_not()
        while self.current_token is not None and self.current_token[0] in ['AND','OR']:
            op = self.current_token[0]
            self.advance()
            right = self.parse_not()
            left = {
                    'type':'binary_operation',
                    'op':op,
                    'left':left,
                    'right':right
                    }
        return left
    