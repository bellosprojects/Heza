import os
from funciones import funs as specialsFuns, process_special, process_methods, methods

import math

class Heza():
    def __init__(self,ast):
        self.ast = ast
        self.vars = {'PI':math.pi,'E':math.e}
        self.traces = {}
        self.funs = []
        self.loops = []

    def Error(self,msg):
        print(msg)
        exit()

    def get_value(self, value):
        if not value:
            return None
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
            return value['valor'][1:-1]
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
            elif value['op'] == 'DISTINTO':
                return self.get_value(value['left']) != self.get_value(value['right'])
            elif value['op'] == 'MAYOR':
                return self.get_value(value['left']) > self.get_value(value['right'])
            elif value['op'] == 'MENOR':
                return self.get_value(value['left']) < self.get_value(value['right'])
            elif value['op'] == 'MAYORE':
                return self.get_value(value['left']) >= self.get_value(value['right'])
            elif value['op'] == 'MENORE':
                return self.get_value(value['left']) <= self.get_value(value['right'])
        elif value['type'] == 'unary_operation':
            if value['op'] == 'NOT':
                return not self.get_value(value['valor'])
            elif value['op'] == 'RESTA':
                return -self.get_value(value['valor'])
            elif value['op'] == 'SUMA':
                return self.get_value(value['valor'])
        elif value['type'] == 'trace':
            if not value['valor'] in self.traces:
                self.Error("Undefined trace: " + value['valor'])
                exit()
            valor = self.traces.get(value['valor'])
            return valor
            
        return None
            
    def print_(self, valores):
        for valor in valores:
            print(str(self.get_value(valor)),end="",flush=True)

    def getByConsole(self):
        value = ""
        while value == "":
            value = input()

        if value.isdecimal():
            value = float(value)
            if value.is_integer():
                value = int(value)
        return value

    def input_(self, ids):
        for id_ in ids:
            if id_ in self.vars:
                valor = self.getByConsole()
                self.vars[id_] = valor
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
            self.vars[id_['name']] = self.get_value(id_['value'])
            if trace:
                self.traces[id_['name']] = f"{id_['name']} = {self.get_value(id_['value'])}"

    def clear(self):
        os.system('cls()')

    def condicional(self,condicion,body):
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

    def call(self,name,args):
        named = None

        if name in specialsFuns:
            if len(args) != specialsFuns[name]:
                self.Error(f"La funcion '{name}' requiere {specialsFuns[name]} argumentos y se le estan enviando {len(args)}") 
            else:
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

    def process(self,commad):
        if commad['type'] == 'data_declaration':
            self.data_declaration(commad['variables'],commad['trace'])
        elif commad['type'] == 'entrada':
            self.input_(commad['variables'])
        elif commad['type'] == 'salida':
            self.print_(commad['datos'])
        elif commad['type'] == 'reasignacion':
            self.asignacion_(commad['variables'],commad['valores'])
        elif commad['type'] == 'CLS':
            self.clear()
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

    def run(self):
        for commad in self.ast['program']:
            self.process(commad)

    def debug(self):
        print(f"\nVars: {self.vars}")
        print(f"traces: {self.traces}")
        print(f"funcs: {self.funs}")