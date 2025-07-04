import random, time
import msvcrt
import math, sys
import keyboard, datetime

funs = {'Integer':1,
        'String':1,
        'R':2,
        'Wait':1,
        'KEY':0,
        'Size':1,
        'Sin':1,
        'Cos':1,
        'Sqrt':1,
        'Ln':1,
        'Log':2,
        'ToUpperCase':1,
        'ToLowerCase':1,
        'Pressed':1,
        'Vocals':1,
        'Equals':2,
        'Abs':1,
        'Date':0,
        'Time':0,
        'Repeat':2
        }

def process_special(name, parametros):
    if name == 'Integer':
        return int(parametros[0])
    elif name == 'String':
        return str(parametros[0])
    elif name == 'R':
        return random.randint(parametros[0],parametros[1])
    elif name == 'Wait':
        sys.stdout.flush()
        time.sleep(parametros[0])
    elif name == 'KEY':
        sys.stdout.flush()
        msvcrt.getch()
    elif name == 'Size':
        return len(str(parametros[0]))
    elif name == 'Sin':
        return math.sin(parametros[0])
    elif name == 'Cos':
        return math.cos(parametros[0])
    elif name == 'Sqrt':
        return math.sqrt(parametros[0])
    elif name == 'Ln':
        return math.log(parametros[0])
    elif name == 'Log':
        return math.log(parametros[0],parametros[1])
    elif name == 'ToUpperCase':
        return str(parametros[0]).upper()
    elif name == 'ToLowerCase':
        return str(parametros[0]).lower()
    elif name == 'Pressed':
        return keyboard.is_pressed(parametros[0])
    elif name == 'Vocals':
        v = ""
        for i in str(parametros[0]):
            if i.lower() in 'aeiou':
                v += i
        return v
    elif name == 'Abs':
        return abs(parametros[0])
    elif name == 'Date':
        return str(datetime.datetime.now().strftime("%a %d-%b-%Y"))
    elif name == 'Time':
        return str(datetime.datetime.now().strftime("%H:%M:%S %p"))
    elif name == 'Repeat':
        return str(parametros[0]) * int(parametros[1])

methods = {
    'Reverse':0,
    'Equals':1
}

def process_methods(name, id_, parametros):
    if name == 'Reverse':
        return str(id_)[::-1]
    elif name == 'Equals':
        return str(id_).count(str(parametros[0]))