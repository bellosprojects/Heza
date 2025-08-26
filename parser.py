from tokens import ExpresionValues, ExpresionList, ExpresionExpr
import sys

class Parser:
    def __init__(self, tokens, ist_limit=False):
        self.tokens = tokens
        self.pos = 0
        self.current_token = tokens[0] if tokens else None
        self.it_limit = ist_limit
        sys.set_int_max_str_digits(43000)

    def advance(self):
        self.pos += 1
        self.current_token = self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def Error(self, msg):
        print("\n"+msg)
        exit()

    def parse(self):
        return self.parse_program()
    
    def parse_program(self):

        if self.it_limit:
            return self.parse_logico()

        program = []
        while self.current_token is not None:
            init = self.parse_init()
            program.append(init)

        return {"program": program}

    def parse_init(self,ret=False):
        if self.current_token[0] == 'DATA':
            return self.parse_data()
        elif self.current_token[0] == 'ID':

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
        
        elif self.current_token[0] == 'OUT':
            return self.parse_out()
        elif self.current_token[0] == 'INPUT':
            return self.parse_input()
        elif self.current_token[0] == 'RETURN':
            return self.parse_arrow()
        elif self.current_token[0] == 'FOREACH':
            return self.parse_foreach()

        else:
            self.Error(f"Error de sintaxis: {self.current_token[1]} inesperado")

    def parse_foreach(self):
        self.advance()

        if not self.current_token or self.current_token[0] != 'ID':
            self.Error("Error se esperab un nombre de variable")
        
        var = self.current_token[1]
        self.advance()

        if not self.current_token or self.current_token[0] != 'IN':
            self.Error("Error, se esperaba operador IN")
        self.advance()

        if not self.current_token or (self.current_token[0] not in ExpresionList):
            self.Error("Se esperaba un areglo")
        
        arr = self.parse_logico()

        body = []

        if not self.current_token or self.current_token[0] not in ['UNIQUE','REFERENCE']:
            self.Error("Error, se esperaba el operador REFERENCE o UNIQUE despues de FOREACH")
        
        if self.current_token[0] == 'UNIQUE':
            self.advance()

            if not self.current_token:
                self.Error("Se esperaba una instruccion para UNIQUE en FOREACH")

            body.append(self.parse_init())

        elif self.current_token[0] == 'REFERENCE':
            self.advance()
            while self.current_token:
                if self.current_token[0] == 'END':
                    self.advance()
                    break
                body.append(self.parse_init())

            if not self.current_token or self.current_token[0] != 'REFERENCE':
                self.Error("Se esperaba REFERENCE despues de end")
            self.advance()

            if not self.current_token or self.current_token[0] != 'ID':
                self.Error("Se esperaba un alias despues de end")
            
            if self.current_token[1] != var:
                self.Error("Error, los alias no coinciden")

            self.advance()

        return {'type':'foreach','arr':arr,'accion':body,'var':var}

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

    def parse_input(self):

        if not self.current_token or self.current_token[0] != 'INPUT':
            self.Error("Error de sintaxis: se esperaba un operador de entrada")
        self.advance()

        if not self.current_token or self.current_token[0] != 'ID':
            self.Error("Error de sintaxis, se espeaba una o mas variables")

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

    def parse_subjet(self):
        var = self.current_token[1]
        self.advance()
        self.advance()

        if not self.current_token or self.current_token[0] not in ExpresionList:
            self.Error("Error se esperaba un arreglo para Subjet")
        
        arr = self.parse_logico()

        if not self.current_token or self.current_token[0] != 'REFERENCE':
            self.Error("Error se esperaba :")
        self.advance()

        if not self.current_token:
            self.Error("Se esparab una expresion para Subjet")
        
        expresion = self.parse_logico()

        if not self.current_token or self.current_token[0] != 'CLOSEL':
            self.Error("Se esperaba cerrar llaves en Subjet")
        self.advance()

        return {'type':'subjet','var':var,'arr':arr,'expresion':expresion}

    def parse_limit(self):
        self.advance()

        if not self.current_token or self.current_token[0] != 'OPENP':
            self.Error("Se esperaba ( despues de limit")
        self.advance()

        if not self.current_token or self.current_token[0] not in ExpresionExpr:
            self.Error("Se esperaba una expresion para LIMIT")
        expr = self.parse_logico()

        #El limite es de la forma limit(expr,var → point)
        if not self.current_token or self.current_token[0] != 'COMA':
            self.Error("Se esperaba una coma despues de expr en limit")
        self.advance()
        if not self.current_token or self.current_token[0] != 'ID':
            self.Error("Se esperaba una variable para limit")
        var = self.current_token[1]
        self.advance()
        if not self.current_token or self.current_token[0] != 'THEN':
            self.Error("Se esperaba → despues de var en limit")
        self.advance()
        if not self.current_token:
            self.Error("Se esperaba un punto para limit")
        point = self.parse_logico()

        if not self.current_token or self.current_token[0] != 'CLOSEP':
            self.Error("Se esperaba cerrar parentesis despues de limit")
        self.advance()

        return {'type':'limit','expr':expr,'var':var,'point':point}
    
    def parse_eval(self):
        self.advance()

        #Eval evalua una expresion con una variable a un valor
        #De la forma eval(expr, var → value)

        if not self.current_token or self.current_token[0] != 'OPENP':
            self.Error("Se esperaba ( despues de eval")
        self.advance()

        if not self.current_token or self.current_token[0] not in ExpresionExpr:
            self.Error("Se esperaba una expresion para eval")
        expr = self.parse_logico()

        if self.current_token and self.current_token[0] == 'CLOSEP':
            self.advance()
            return {'type':'evalOnly','expr':expr}

        if not self.current_token or self.current_token[0] != 'COMA':
            self.Error("Se esperaba una coma despues de expr en eval")
        self.advance()

        if not self.current_token or self.current_token[0] != 'ID':
            self.Error("Se esperaba una variable para eval")
        var = self.current_token[1]
        self.advance()

        if not self.current_token or self.current_token[0] != 'THEN':
            self.Error("Se esperaba → despues de var en eval")
        self.advance()

        if not self.current_token:
            self.Error("Se esperaba un valor para eval")

        value = self.parse_logico()

        if not self.current_token or self.current_token[0] != 'CLOSEP':
            self.Error("Se esperaba cerrar parentesis despues de eval")
        self.advance()

        return {'type':'eval','expr':expr,'var':var,'value':value}

    def parse_term(self):
        if self.current_token is not None and self.current_token[0]=='NONE':
            self.advance()
            return {'type':'none'}
        elif self.current_token is not None and self.current_token[0] == 'DERIVATIVE':
            self.advance()
            if not self.current_token or self.current_token[0] != 'OPENP':
                self.Error("Se esperaba ( despues de derivative")
            self.advance()

            if not self.current_token or self.current_token[0] not in ExpresionExpr:
                self.Error("Se esperaba una expresion para derivative")
            expr = self.parse_logico()

            if not self.current_token or self.current_token[0] != 'COMA':
                self.Error("Se esperaba una coma despues de expr en derivative")
            self.advance()

            if not self.current_token or self.current_token[0] != 'ID':
                self.Error("Se esperaba una variable para derivative")
            var = self.current_token[1]
            self.advance()

            if not self.current_token or self.current_token[0] != 'CLOSEP':
                self.Error("Se esperaba cerrar parentesis despues de derivative")
            self.advance()

            return {'type':'derivative','expr':expr,'var':var}
        
        elif self.current_token is not None and self.current_token[0] == 'INTEGRAL':
            self.advance()
            
            #Integral de la forma ∫(expr, var → [a..b])
            if not self.current_token or self.current_token[0] != 'OPENP':
                self.Error("Se esperaba ( despues de integral")
            self.advance()

            if not self.current_token or self.current_token[0] not in ExpresionExpr:
                self.Error("Se esperaba una expresion para integral")
            expr = self.parse_logico()

            if not self.current_token or self.current_token[0] != 'COMA':
                self.Error("Se esperaba una coma despues de expr en integral")
            self.advance()
            if not self.current_token or self.current_token[0] != 'ID':
                self.Error("Se esperaba una variable para integral")
            var = self.current_token[1]
            self.advance()

            if self.current_token and self.current_token[0] == 'CLOSEP':
                #Caso de integral indefinida
                self.advance()
                return {'type':'integralI','expr':expr,'var':var}

            if not self.current_token or self.current_token[0] != 'IN':
                self.Error("Se esperaba → despues de var en integral")
            self.advance()
            if not self.current_token or self.current_token[0] != 'OPENC':
                self.Error("Se esperaba un rango para integral")

            arr = self.parse_logico()
            if not self.current_token or self.current_token[0] != 'CLOSEP':
                self.Error("Se esperaba cerrar parentesis despues de integral")
            self.advance()

            return {'type':'integralD','expr':expr,'var':var,'arr':arr}

        elif self.current_token is not None and self.current_token[0] == 'EXPRESION':
            valor = self.current_token[1]
            self.advance()
            return {'type':'expresion','valor':valor}
        elif self.current_token is not None and self.current_token[0] == 'INFINITE':
            self.advance()
            return {'type':'infinite'}
        elif self.current_token is not None and self.current_token[0] == 'BARRA':
            self.advance()
            if not self.current_token:
                self.Error("Se esperaba un valor para Abs")
            value = self.parse_logico()
            if not self.current_token or self.current_token[0] != 'BARRA':
                self.Error("Se esparab | para terminar Abs")
            self.advance()

            return {'type':'abs','valor':value}

        elif self.current_token is not None and self.current_token[0]=='NUMBER':
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

            if nombre == 'lim':
                return self.parse_limit()
            elif nombre == 'eval':
                return self.parse_eval()

            self.advance()

            if self.current_token and self.current_token[0] == 'OPENP':
                self.advance()
                return self.parse_call(nombre)
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
        elif self.current_token is not None and self.current_token[0] == 'SUMMATION':
            self.advance()
            if not self.current_token or self.current_token[0] != 'OPENP':
                self.Error("Se esperaba '(' despues de summation")
            self.advance()

            if not self.current_token or self.current_token[0] != 'ID':
                self.Error("Error, se esperab una variable en SUMMATION")

            var = self.current_token[1]
            self.advance()

            if not self.current_token or self.current_token[0] != 'IN':
                self.Error("Se esperaba IN para summation")
            self.advance()

            if not self.current_token or self.current_token[0] not in ExpresionList:
                self.Error("Se esperaba un valor para arr en summation")
            arr_value = self.parse_logico()

            if not self.current_token or self.current_token[0] != 'COMA':
                self.Error("Se esperaba una coma despues de FROM en summation")
            self.advance()

            if not self.current_token:
                self.Error("Se esperaba un valor para VALUE en summation")
            value = self.parse_logico()
            if not self.current_token or self.current_token[0] != 'CLOSEP':
                self.Error("Se esperaba cerra parentesis despues de summation")
            self.advance()

            return {'type':'summation','arr':arr_value,'valor':value,'var':var}

        elif self.current_token is not None and self.current_token[0] == 'PRODUCTION':
            self.advance()
            if not self.current_token or self.current_token[0] != 'OPENP':
                self.Error("Se esperaba '(' despues de production")
            self.advance()

            if not self.current_token or self.current_token[0] != 'ID':
                self.Error("Error, se esperaba una variable en production")

            var = self.current_token[1]
            self.advance()

            if not self.current_token or self.current_token[0] != 'IN':
                self.Error("Se esperaba IN para production")
            self.advance()

            if not self.current_token or self.current_token[0] not in ExpresionList:
                self.Error("Se esperaba un valor para arr en production")
            arr_value = self.parse_logico()

            if not self.current_token or self.current_token[0] != 'COMA':
                self.Error("Se esperaba una coma despues de FROM en production")
            self.advance()

            if not self.current_token:
                self.Error("Se esperaba un valor para VALUE en production")
            value = self.parse_logico()
            if not self.current_token or self.current_token[0] != 'CLOSEP':
                self.Error("Se esperaba cerra parentesis despues de production")
            self.advance()

            return {'type':'production','arr':arr_value,'valor':value,'var':var}

        elif self.current_token is not None and self.current_token[0] == 'OPENL':
            self.advance()

            if not self.current_token:
                self.Error("Error se esperaba un valor despues de '{'")

            if self.pos < len(self.tokens) and self.tokens[self.pos][0] == 'ID':
                if self.pos + 1 < len(self.tokens) and self.tokens[self.pos+1][0] == 'IN':
                    is_sub = False
                    num = self.pos+2
                    llaves = 0
                    while num < len(self.tokens):
                        if self.tokens[num][0] == 'OPENL':
                            llaves += 1
                        if self.tokens[num][0] == 'CLOSEL':
                            llaves -= 1
                        if self.tokens[num][0] == 'COMA' and llaves == 0:
                            break
                        if self.tokens[num][0] == 'REFERENCE':
                            is_sub = True
                            break
                        num += 1

                    if is_sub:
                        return self.parse_subjet()

            values = []

            while self.current_token[0] in ExpresionValues:
                valor = self.parse_logico()
                values.append(valor)

                if not self.current_token or self.current_token[0] != 'COMA':
                    break
                self.advance()

            if not self.current_token or self.current_token[0] != 'CLOSEL':
                self.Error("Se esperaba '}' despues de los elementos de la lista")
            self.advance()

            return {'type':'list','valor':values}
        
        elif self.current_token and self.current_token[0] == 'OPENC':
            self.advance()

            if not self.current_token:
                self.Error("Error se esperaba un valor numerico para FROM en []")
            
            from_value = self.parse_logico()

            if not self.current_token or self.current_token[0] != 'PUNTO':
                self.Error("Error se esperaba operador de rango '..' para []")
            self.advance()

            if not self.current_token or self.current_token[0] != 'PUNTO':
                self.Error("Error se esperaba operador de rango '..' para []")
            self.advance()

            if not self.current_token:
                self.Error("Error se esperab un valor numerico para TO en []")
            
            to_value = self.parse_logico()

            if not self.current_token:
                self.Error("Error, se esperaba cerrar el rango []")

            if self.current_token[0] == 'CLOSEC':
                self.advance()
                return {'type':'range','from':from_value,'to':to_value}
            
            if self.current_token[0] != 'REFERENCE':
                self.Error("Error se esperaba cerra el rango []")

            self.advance()

            if not self.current_token:
                self.Error("Se esparaba valor para step en rango []")

            step = self.parse_logico()

            if not self.current_token or self.current_token[0] != 'CLOSEC':
                self.Error("Se esperaba cerrar el rango []")

            self.advance()

            return {'type':'range','from':from_value,'to':to_value,'step':step}
        
        elif self.current_token and self.current_token[0] == 'FOREACH':
            self.advance()

            if not self.current_token or self.current_token[0] != 'ID':
                self.Error("Se esperaba una variable para foreach")
            
            var = self.current_token[1]
            self.advance()

            if not self.current_token or self.current_token[0] != 'IN':
                self.Error("Se esperaba IN en foreach")
            self.advance()

            if not self.current_token or (self.current_token[0] not in ExpresionList):
                self.Error("Se esperaba un areglo")
            
            arr = self.parse_logico()

            if not self.current_token or self.current_token[0] != 'REFERENCE':
                self.Error("Se esperaba : en foreach")
            self.advance()

            if not self.current_token:
                self.Error("Se esperaba una expresion")
            
            expresion = self.parse_logico()

            return {'type':'foreach','arr':arr,'var':var,'expresion':expresion}
                
        elif self.current_token and self.current_token[0] == 'EXIST':
            self.advance()

            if not self.current_token or self.current_token[0] != 'ID':
                self.Error("Se esperaba una variable para foreach")
            
            var = self.current_token[1]
            self.advance()

            if not self.current_token or self.current_token[0] != 'IN':
                self.Error("Se esperaba IN en foreach")
            self.advance()

            if not self.current_token or (self.current_token[0] not in ExpresionList):
                self.Error("Se esperaba un areglo")
            
            arr = self.parse_logico()

            if not self.current_token or self.current_token[0] != 'REFERENCE':
                self.Error("Se esperaba : en foreach")
            self.advance()

            if not self.current_token:
                self.Error("Se esperaba una expresion")
            
            expresion = self.parse_logico()

            return {'type':'exist','arr':arr,'var':var,'expresion':expresion}

        else:
            self.Error("Se esperaba una expresion")

    def parse_parentesis(self):
        if self.current_token is not None and self.current_token[0] == 'OPENP':
            self.advance()
            expr = self.parse_logico()
            if self.current_token is not None and self.current_token[0] == 'CLOSEP':
                self.advance()
                return expr
            else:
                self.Error("Error de sintaxis: se esperaba un parentesis cerrado")
        else:
            return self.parse_term()
    
    def parse_unary(self):
        if self.current_token is not None and self.current_token[0] in ['RESTA','SUMA','EXC','SQRT']:
            op = self.current_token[0]
            self.advance()
            expr = self.parse_parentesis()
            return {
                    'type':'unary_operation',
                    'op':op,
                    'valor':expr
                    }
        else:
            return self.parse_parentesis()
    
    def parse_pow(self):
        left = self.parse_unary()
        while self.current_token is not None and self.current_token[0] in ['POW']:
            op = self.current_token[0]
            self.advance()
            right = self.parse_unary()
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
        while self.current_token is not None and self.current_token[0] in ['COMPARACION','DIFFERENT','MAYORE','MENORE','MAYOR','MENOR','IN']:
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
        if self.current_token is not None and self.current_token[0] in ['NOT']:
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
    