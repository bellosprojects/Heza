from funciones import funs as specialsFuns, process_special, process_methods, methods
import sympy as sp
from expr import Expresion
from funciones import conversionOutTableToSymbols as cts

import math

class Heza():
    def __init__(self,ast):
        self.ast = ast
        self.traces = {'condition':"condition = False"}
        self.funs = []
        self.loops = []
        self.vars = {'PI':math.pi,'E':math.e,'condition':False}

    def Error(self,msg):
        print("\n"+msg)
        exit()

    def sympy_to_heza(self, expr):

        return expr.replace("**", '^').replace('oo', '∞').replace('sqrt', '√').replace(' ','')

    def heza_to_sympy(self, expr, var):
        if expr['type'] == 'number':
            return expr['valor']
        elif expr['type'] == 'id':
            if expr['valor'] == var and var is not None:
                return sp.symbols(var)
            elif expr['valor'] in self.vars and (isinstance(self.vars[expr['valor']], int) or isinstance(self.vars[expr['valor']], float) or isinstance(self.vars[expr['valor']], Expresion) or isinstance(self.vars[expr['valor']], str)):
                if isinstance(self.vars[expr['valor']], Expresion):
                    return self.heza_to_sympy(self.vars[expr['valor']].to_ast(), var)
                elif isinstance(self.vars[expr['valor']], str):
                    return self.heza_to_sympy(Expresion(self.vars[expr['valor']]).to_ast(), var)
                return self.vars[expr['valor']]
            else:
                return sp.symbols(expr['valor'])
        elif expr['type'] == 'infinite':
            return sp.oo
        elif expr['type'] == 'binary_operation':
            left = self.heza_to_sympy(expr['left'], var)
            right = self.heza_to_sympy(expr['right'], var)
            if expr['op'] == 'SUMA':
                return left + right
            elif expr['op'] == 'RESTA':
                return left - right
            elif expr['op'] == 'MULTIPLICACION':
                return left * right
            elif expr['op'] == 'DIVISION':
                return left / right
            elif expr['op'] == 'POW':
                return left ** right
            elif expr['op'] == 'MOD':
                return left % right
        elif expr['type'] == 'unary_operation':
            valor = self.heza_to_sympy(expr['valor'], var)
            if expr['op'] == 'RESTA':
                return -valor
            elif expr['op'] == 'SUMA':
                return valor
            elif expr['op'] == 'SQRT':
                return sp.sqrt(valor)
            elif expr['op'] == 'EXC':
                return sp.factorial(valor)
        elif expr['type'] == 'abs':
            return sp.Abs(self.heza_to_sympy(expr['valor'], var))
        elif expr['type'] == 'infinite':
            return sp.oo
        elif expr['type'] == 'parentesis':
            return self.heza_to_sympy(expr['valor'], var)
        elif expr['type'] == 'call':

            if expr['name'] == 'sin':
                if len(expr['args']) != 1:
                    self.Error("La funcion 'sin' requiere 1 argumento")
                return sp.sin(self.heza_to_sympy(expr['args'][0], var))
            elif expr['name'] == 'cos':
                if len(expr['args']) != 1:
                    self.Error("La funcion 'cos' requiere 1 argumento")
                return sp.cos(self.heza_to_sympy(expr['args'][0], var))
            
            elif expr['name'] == 'tan':
                if len(expr['args']) != 1:
                    self.Error("La funcion 'tan' requiere 1 argumento")
                return sp.tan(self.heza_to_sympy(expr['args'][0], var))
            elif expr['name'] == 'log':
                if len(expr['args']) < 1 or len(expr['args']) > 2:
                    self.Error("La funcion 'log' requiere 1 o 2 argumentos")
                base = math.e if len(expr['args']) == 1 else self.heza_to_sympy(expr['args'][1], var)
                return sp.log(self.heza_to_sympy(expr['args'][0], var), base)
            elif expr['name'] == 'ln':
                if len(expr['args']) != 1:
                    self.Error("La funcion 'ln' requiere 1 argumento")
                return sp.ln(self.heza_to_sympy(expr['args'][0], var))
            elif expr['name'] == 'exp':
                if len(expr['args']) != 1:
                    self.Error("La funcion 'exp' requiere 1 argumento")
                return sp.exp(self.heza_to_sympy(expr['args'][0], var))
            elif expr['name'] == 'cosec':
                if len(expr['args']) != 1:
                    self.Error("La funcion 'cosec' requiere 1 argumento")
                return 1/sp.sin(self.heza_to_sympy(expr['args'][0], var))
            elif expr['name'] == 'sec':
                if len(expr['args']) != 1:
                    self.Error("La funcion 'sec' requiere 1 argumento")
                return 1/sp.cos(self.heza_to_sympy(expr['args'][0], var))
            elif expr['name'] == 'cotan':
                if len(expr['args']) != 1:
                    self.Error("La funcion 'cotan' requiere 1 argumento")
                return 1/sp.tan(self.heza_to_sympy(expr['args'][0], var))
            elif expr['name'] == 'arcsin':
                if len(expr['args']) != 1:
                    self.Error("La funcion 'arcsin' requiere 1 argumento")
                return sp.asin(self.heza_to_sympy(expr['args'][0], var))
            elif expr['name'] == 'arccos':
                if len(expr['args']) != 1:
                    self.Error("La funcion 'arccos' requiere 1 argumento")
                return sp.acos(self.heza_to_sympy(expr['args'][0], var))
            elif expr['name'] == 'arctan':
                if len(expr['args']) != 1:
                    self.Error("La funcion 'arctan' requiere 1 argumento")
                return sp.atan(self.heza_to_sympy(expr['args'][0], var))
            elif expr['name'] == 'sinh':
                if len(expr['args']) != 1:
                    self.Error("La funcion 'sinh' requiere 1 argumento")
                return sp.sinh(self.heza_to_sympy(expr['args'][0], var))
            elif expr['name'] == 'cosh':
                if len(expr['args']) != 1:
                    self.Error("La funcion 'cosh' requiere 1 argumento")
                return sp.cosh(self.heza_to_sympy(expr['args'][0], var))
            elif expr['name'] == 'tanh':
                if len(expr['args']) != 1:
                    self.Error("La funcion 'tanh' requiere 1 argumento")
                return sp.tanh(self.heza_to_sympy(expr['args'][0], var))
            elif expr['name'] == 'asinh':
                if len(expr['args']) != 1:
                    self.Error("La funcion 'asinh' requiere 1 argumento")
                return sp.asinh(self.heza_to_sympy(expr['args'][0], var))
            elif expr['name'] == 'acosh':
                if len(expr['args']) != 1:
                    self.Error("La funcion 'acosh' requiere 1 argumento")
                return sp.acosh(self.heza_to_sympy(expr['args'][0], var))
            elif expr['name'] == 'atanh':
                if len(expr['args']) != 1:
                    self.Error("La funcion 'atanh' requiere 1 argumento")
                return sp.atanh(self.heza_to_sympy(expr['args'][0], var))
            elif expr['name'] == 'sqrt':
                if len(expr['args']) != 1:
                    self.Error("La funcion 'sqrt' requiere 1 argumento")
                return sp.sqrt(self.heza_to_sympy(expr['args'][0], var))
            elif expr['name'] == 'root':
                if len(expr['args']) != 2:
                    self.Error("La funcion 'root' requiere 2 argumentos")
                return self.heza_to_sympy({'type':'binary_operation','op':'POW','left':expr['args'][0],'right':{'type':'binary_operation','op':'DIVISION','left':{'type':'number','valor':1},'right':expr['args'][1]}}, var)
            elif expr['name'] == 'sign':
                if len(expr['args']) != 1:
                    self.Error("La funcion 'sign' requiere 1 argumento")
                return sp.sign(self.heza_to_sympy(expr['args'][0], var))

            return self.call(expr['name'], expr['args'], True)
        elif expr['type'] == 'summation':
            var = expr['var']
            if expr['arr']['type'] != 'range':
                self.Error("El parametro ARR en summation debe ser un rango")
            limitA = self.heza_to_sympy(expr['arr']['from'], var)
            limitB = self.heza_to_sympy(expr['arr']['to'], var)
            return sp.summation(self.heza_to_sympy(expr['valor'], var), (sp.symbols(var), limitA, limitB))
        elif expr['type'] == 'production':
            var = expr['var']
            if expr['arr']['type'] != 'range':
                self.Error("El parametro ARR en production debe ser un rango")
            limitA = self.heza_to_sympy(expr['arr']['from'], var)
            limitB = self.heza_to_sympy(expr['arr']['to'], var)
            return sp.product(self.heza_to_sympy(expr['valor'], var), (sp.symbols(var), limitA, limitB))
        elif expr['type'] == 'expresion':
            valor = Expresion(expr['valor']).to_ast()
            return self.heza_to_sympy(valor, var)
        
        elif expr['type'] == 'eval':
            expr_inner = self.heza_to_sympy(expr['expr'], var)
            val = self.heza_to_sympy(expr['value'], var)
            var_inner = expr['var']
            if isinstance(expr_inner, int) or isinstance(expr_inner, float):
                expr_inner = sp.Integer(expr_inner)
            result = expr_inner.subs(sp.symbols(var_inner), val)
            try:
                result = result.evalf()
            except:
                pass
            return result
        
        elif expr['type'] == 'evalOnly':
            expr_inner = self.heza_to_sympy(expr['expr'], var)
            if isinstance(expr_inner, int) or isinstance(expr_inner, float):
                expr_inner = sp.Integer(expr_inner)
            result = expr_inner.subs({})
            try:
                result = result.evalf()
            except:
                pass
            return result
        
        elif expr['type'] == 'limit':
            expr_inner = self.heza_to_sympy(expr['expr'], var)
            point = self.heza_to_sympy(expr['point'], var)
            var_inner = expr['var']
            return sp.limit(expr_inner, sp.symbols(var_inner), point)
        
        elif expr['type'] == 'derivative':
            expr_inner = self.heza_to_sympy(expr['expr'], var)
            var_inner = expr['var']
            return sp.diff(expr_inner, sp.symbols(var_inner))
        
        elif expr['type'] == 'integralI':
            expr_inner = self.heza_to_sympy(expr['expr'], var)
            var_inner = expr['var']
            return sp.integrate(expr_inner, sp.symbols(var_inner))
        
        elif expr['type'] == 'integralD':
            expr_inner = self.heza_to_sympy(expr['expr'], var)
            a = self.heza_to_sympy(expr['arr']['from'], var)
            b = self.heza_to_sympy(expr['arr']['to'], var)
            var_inner = expr['var']
            return sp.integrate(expr_inner, (sp.symbols(var_inner), a, b))
        
        return None
    
    def limit(self, expr, var, point):
        expr_sympy = self.heza_to_sympy(expr.to_ast(), var)
        return sp.limit(expr_sympy, sp.symbols(var), point)

    def get_value(self, value):
        if not value or value['type'] == 'none':
            return None

        if value['type'] == 'derivative':
            expr = self.get_value(value['expr'])
            var = value['var']
            expr_sympy = self.heza_to_sympy(expr.to_ast(), var)
            result = str(sp.diff(expr_sympy, sp.symbols(var)))

            if result.startswith('Derivative('):
                self.Error("No se pudo calcular la derivada")

            return Expresion(self.sympy_to_heza(result))

        if value['type'] == 'integralI':
            expr = self.get_value(value['expr'])
            var = value['var']
            expr_sympy = self.heza_to_sympy(expr.to_ast(), var)
            result = str(sp.integrate(expr_sympy, sp.symbols(var)))
            if result.startswith('Integral('):
                self.Error("No se pudo calcular la integral indefinida")
            return Expresion(self.sympy_to_heza(result))
        
        if value['type'] == 'integralD':
            #Integral definida
            expr = self.get_value(value['expr'])
            var = value['var']
            a = self.get_value(value['arr']['from'])
            b = self.get_value(value['arr']['to'])
            expr_sympy = self.heza_to_sympy(expr.to_ast(), var)
            result = str(sp.integrate(expr_sympy, (sp.symbols(var), a, b)))

            if result.startswith('Integral('):
                self.Error("No se pudo calcular la integral definida")
            return int(result)

        if value['type'] == 'expresion':
            return Expresion(value['valor'])

        if value['type'] == 'infinite':
            return math.inf

        if value['type'] == 'limit':
            result = str(self.limit(self.get_value(value['expr']), value['var'], self.get_value(value['point'])))
            
            if result.startswith('Limit('):
                self.Error("No se pudo calcular el limite")
            
            return Expresion(self.sympy_to_heza(result))
        
        if value['type'] == 'eval':
            expr = self.get_value(value['expr'])
            val = self.get_value(value['value'])
            var = value['var']
            return self.eval(expr, val, var)

        if value['type'] == 'evalOnly':
            expr = self.get_value(value['expr'])
            return self.evalOnly(expr)

        if value['type'] == 'subjet':
            arr = self.get_value(value['arr'])
            final = []
            for i in arr:
                self.vars[value['var']] = i
                if bool(self.get_value(value['expresion'])):
                    final.append(i)

            del self.vars[value['var']]
            return final

        if value['type'] == 'foreach':
            arr = self.get_value(value['arr'])
            self.vars[value['var']] = arr[0]
            final = bool(self.get_value(value['expresion']))
            for i in arr:
                self.vars[value['var']] = i
                final = final and bool(self.get_value(value['expresion']))
            
            del self.vars[value['var']]
            return final

        if value['type'] == 'exist':
            arr = self.get_value(value['arr'])
            self.vars[value['var']] = arr[0]
            final = bool(self.get_value(value['expresion']))
            for i in arr:
                self.vars[value['var']] = i
                final = final or bool(self.get_value(value['expresion']))
            
            del self.vars[value['var']]
            return final

        if value['type'] == 'abs':
            return abs(self.get_value(value['valor']))
        if value['type'] == 'method':
            return self.method(value['id'],value['function'],value['args'])
        if value['type'] == 'call':
            return self.call(value['name'],value['args'])
        if value['type'] == 'id':
            if value['valor'] not in self.vars:
                self.Error("Undefined variable: " + value['valor'])

            valor = self.vars.get(value['valor']) 
            return valor
        if value['type'] in ['number','boolean','constant']:
            return value['valor']
        elif value['type'] == 'str':
            return value['valor']
        elif value['type'] == 'binary_operation':
            if value['op'] == 'SUMA':
                return self.get_value(value['left']) + self.get_value(value['right'])
            elif value['op'] == 'RESTA':
                return self.get_value(value['left']) - self.get_value(value['right'])
            elif value['op'] == 'MULTIPLICACION':
                return self.get_value(value['left']) * self.get_value(value['right'])
            elif value['op'] == 'DIVISION':
                return self.get_value(value['left']) / self.get_value(value['right'])
            elif value['op'] == 'MOD':
                return self.get_value(value['left']) % self.get_value(value['right'])
            elif value['op'] == 'POW':
                return (self.get_value(value['left'])) ** (self.get_value(value['right']))
            elif value['op'] == 'AND':
                return self.get_value(value['left']) and self.get_value(value['right'])
            elif value['op'] == 'OR':
                return self.get_value(value['left']) or self.get_value(value['right'])
            elif value['op'] == 'COMPARACION':
                return self.get_value(value['left']) == self.get_value(value['right'])
            elif value['op'] == 'DIFFERENT':
                return self.get_value(value['left']) != self.get_value(value['right'])
            elif value['op'] == 'MAYOR':
                return self.get_value(value['left']) > self.get_value(value['right'])
            elif value['op'] == 'MENOR':
                return self.get_value(value['left']) < self.get_value(value['right'])
            elif value['op'] == 'MAYORE':
                return self.get_value(value['left']) >= self.get_value(value['right'])
            elif value['op'] == 'MENORE':
                return self.get_value(value['left']) <= self.get_value(value['right'])
            elif value['op'] == 'IN':
                return self.get_value(value['left']) in self.get_value(value['right'])
        elif value['type'] == 'unary_operation':
            if value['op'] == 'NOT':
                return not self.get_value(value['valor'])
            elif value['op'] == 'RESTA':
                return -self.get_value(value['valor'])
            elif value['op'] == 'SUMA':
                return self.get_value(value['valor'])
            elif value['op'] == 'EXC':
                return math.factorial(self.get_value(value['valor']))
            elif value['op'] == 'SQRT':
                return math.sqrt(self.get_value(value['valor']))
        elif value['type'] == 'trace':
            if not value['valor'] in self.traces:
                self.Error("Undefined trace: " + value['valor'])
                exit()
            valor = self.traces.get(value['valor'])
            return valor
        elif value['type'] == 'summation':
            return self.summation(value)
        elif value['type'] == 'parentesis':
            return self.get_value(value['valor'])
        elif value['type'] == 'production':
            return self.production(value)
        elif value['type'] == 'list':
            return [self.get_value(element) for element in value['valor']]
        elif value['type'] == 'range':
            from_value = self.get_value(value['from'])
            to_value = self.get_value(value['to'])

            step = value.get('step', '')
            if not step:
                step = 1
            else:
                step = self.get_value(step)

            if not isinstance(from_value, int) and not isinstance(from_value, float):
                self.Error("Error, parametros FROM invalido, debe ser numerico")
            if not isinstance(to_value, int) and not isinstance(to_value, float):
                self.Error("Error, parametros TO invalido, debe ser numerico")
            if not isinstance(step, int) and not isinstance(step, float):
                self.Error("Error, parametros STEP invalido, debe ser numerico")

            if from_value < to_value and step<0:
                return []
            if from_value > to_value and step>0:
                return []

            if step == 0:
                self.Error("Error, el parametro STEP no puede ser 0")
            elif step < 0:
                return list(range(from_value,to_value-1,step))
            return list(range(from_value,to_value+1,step))

        return None

    def evalOnly(self, expr):
        expr_sympy = self.heza_to_sympy(expr.to_ast(), None)
        if isinstance(expr_sympy, int) or isinstance(expr_sympy, float):
            expr_sympy = sp.Number(expr_sympy)

        result = expr_sympy.subs({})
        try:
            result = result.evalf()
        except:
            pass
        return Expresion(self.sympy_to_heza(str(result)))

    def eval(self, expr, value, var):

        expr_sympy = self.heza_to_sympy(expr.to_ast(), var)

        if isinstance(expr_sympy, int) or isinstance(expr_sympy, float):
            expr_sympy = sp.Number(expr_sympy)

        result = expr_sympy.subs(sp.symbols(var), value)
        try:
            result = result.evalf()
        except:
            pass
        return Expresion(self.sympy_to_heza(str(result)))

    def production(self, value):
        arr = self.get_value(value['arr'])

        if not isinstance(arr, list) and not isinstance(arr, str):
            self.Error(f"Valor invalido para ARR en production, '{arr}'")

        result = 1
        for i in arr:
            self.vars[value['var']] = i
            result *= self.get_value(value['valor'])

        if len(arr) > 0:
            del self.vars[value['var']]
        return result

    def summation(self, value):
        arr = self.get_value(value['arr'])

        if not isinstance(arr, list) and not isinstance(arr, str):
            self.Error(f"Valor invalido para ARR en summation, '{arr}'")

        result = 0
        for i in arr:
            self.vars[value['var']] = i
            result += self.get_value(value['valor'])

        del self.vars[value['var']]
        return result

    def print_(self, valores):
        for valor in valores:
            valor = str(self.get_value(valor))
            if valor in cts:
                valor = cts[valor]
            print(valor,end="",flush=True)

    def getByConsole(self):
        value = ''
        while value == '':
            value = input()

        try:
            value = float(value)
            if value.is_integer():
                value = int(value)
        except (TypeError,ValueError):
            pass
        return value

    def input_(self, ids):
        for id_ in ids:
            if id_ in self.vars:
                valor = self.getByConsole()
                self.vars[id_] = valor
                if id_ in self.traces:
                    self.traces[id_] += f" >> {valor}"
            else:
                self.Error(f"Variable '{id_}' no declarada")

    def asignacion_(self,ids,valores,loop=False):
        valores_copy = []
        for valor in valores:
            valores_copy.append(self.get_value(valor))

        for index,id_ in enumerate(ids):
            if id_ not in self.vars and not loop:
                self.Error(f"Variable '{id_}' no declarada")
            self.vars[id_] = valores_copy[index]
            if id_ in self.traces:
                self.traces[id_] += f" >> {valores_copy[index]}"

    def data_declaration(self, ids,trace):
        for id_ in ids:
            if id_['name'] in self.vars:
                self.Error(f"Variable '{id_['name']}' ya declarada")
            self.vars[id_['name']] = self.get_value(id_['value'])
            if trace:
                self.traces[id_['name']] = f"{id_['name']} = {self.get_value(id_['value'])}"

    def condicional(self,condicion,body):
        self.vars['condition'] = self.get_value(condicion)
        if self.get_value(condicion):
            for commad in body:
                val = self.process(commad)
                if val is not None:
                    return val

    def loop(self,start,end,increment,body,alias):
        valor1 = self.get_value(start)
        if valor1:
            valor1 = int(valor1)
        valor2 = self.get_value(end)
        self.asignacion_([alias],[{'type':'number','valor':valor1}],True)

        self.loops.append(alias)
        if valor1 <= valor2:
            while self.get_value({'type':'id','valor':alias}) <= valor2 and alias in self.loops:
                for commad in body:
                    val = self.process(commad)
                    if val is not None:
                        return val
                self.asignacion_([alias],[{'type':'number','valor':abs(self.get_value(increment))+self.get_value({'type':'id','valor':alias})}])
        else:
            while self.get_value({'type':'id','valor':alias}) >= valor2 and alias in self.loops:
                for commad in body:
                    val = self.process(commad)
                    if val is not None:
                        return val
                self.asignacion_([alias],[{'type':'number','valor':-abs(self.get_value(increment))+self.get_value({'type':'id','valor':alias})}])

    def while_(self,condicion,body,alias):
        self.loops.append(alias)
        while self.get_value(condicion) and alias in self.loops:
            for commad in body:
                val = self.process(commad)
                if val is not None:
                    return val

    def function(self,name,args,body):
        self.funs.append({
            'name':name,
            'args':args,
            'body':body
        })

    def call(self,name,args,is_limit=False):
        named = None

        if name in specialsFuns:
            if len(args) != specialsFuns[name]:
                self.Error(f"La funcion '{name}' requiere {specialsFuns[name]} argumentos y se le estan enviando {len(args)}") 
            else:
                if is_limit:
                    self.Error("No se puede usar una funcion especial dentro de un limite")
                return process_special(name, [self.get_value(x) for x in args])

        for fun in self.funs:
            if fun['name'] == name:
                named = fun
        if not named:
            self.Error(f"La funcion '{name}' no esta declarada")

        if len(args) != len(named['args']):
            self.Error(f"La funcion '{name}' requiere {len(named['args'])} argumentos y se le estan enviando {len(args)}") 

        for index,arg in enumerate(args):
            self.vars[named['args'][index]] = self.get_value(arg)

        for commad in named['body']:
            val = self.process(commad)
            if val is not None:
                return val

        for arg in named['args']:
            self.vars.pop(arg)

    def method(self, id_, function, args):

        if function not in methods:
            self.Error(f"El metodo '{function}' no existe")

        if methods[function] != len(args):
            self.Error(f"El metodo '{function}' requiere {methods[function]} argumentos y se le estan enviando {len(args)}")

        return process_methods(function, self.get_value(id_), [self.get_value(x) for x in args])

    def foreach(self, command):
        for x in self.get_value(command['arr']):
            self.vars[command['var']] = x
            for c in command['accion']:
                self.process(c)
        del self.vars[command['var']]

    def process(self,commad):
        if commad['type'] == 'data_declaration':
            self.data_declaration(commad['variables'],commad['trace'])
        elif commad['type'] == 'entrada':
            self.input_(commad['variables'])
        elif commad['type'] == 'salida':
            self.print_(commad['datos'])
        elif commad['type'] == 'reasignacion':
            self.asignacion_(commad['variables'],commad['valores'])
        elif commad['type'] == 'condicional':
            val = self.condicional(commad['condicion'],commad['body'])
            if val is not None:
                return val
        elif commad['type'] == 'loop':
            val  = self.loop(commad['start'],commad['end'],commad['increment'],commad['body'],commad['alias'])
            if val is not None:
                return val
        elif commad['type'] == 'while':
            val = self.while_(commad['condition'],commad['body'],commad['alias'])
            if val is not None:
                return val
        elif commad['type'] == 'function':
            self.function(commad['name'],commad['args'],commad['body'])
        elif commad['type'] == 'call':
            self.call(commad['name'],commad['args'])
        elif commad['type'] == 'return':
            return self.get_value(commad['values'][0])
        elif commad['type'] == 'method':
            self.method(commad['id'],commad['function'],commad['args'])
        elif commad['type'] == 'endnow':
            self.loops.remove(commad['alias'])
        elif commad['type'] == 'foreach':
            self.foreach(commad)

    def run(self):
        for commad in self.ast['program']:
            self.process(commad)

    def debug(self):
        print(f"\nVars: {self.vars}")
        print(f"traces: {self.traces}")
        print(f"funcs: {self.funs}")