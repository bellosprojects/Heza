import random, time
import msvcrt
import math, sys
import keyboard, datetime
import pyttsx3
import speech_recognition
import wikipedia
import os
from expr import Expresion
import sympy as sp

conversionOutTableToSymbols = {
    'inf': '∞',
    'True': 'true',
    'False': 'false',
}

wikipedia.set_lang("es")

funs = {'Integer':1,
        'String':1,
        'R':2,
        'Wait':1,
        'KEY':0,
        'Size':1,
        'Sin':1,
        'Cos':1,
        'Ln':1,
        'log':1,
        'ToUpperCase':1,
        'ToLowerCase':1,
        'Pressed':1,
        'Vocals':1,
        'Equals':2,
        'Date':0,
        'Time':0,
        'Repeat':2,
        'Talk':2,
        'Ear':1,
        'Search':1,
        'system':1,
        'Num':1,
        'Abs':1,
        }

def process_special(name, parametros):
    if name == 'Integer':
        return int(parametros[0])
    elif name == 'Abs':
        return abs(parametros[0])
    elif name == 'Num':
        if isinstance(parametros[0], Expresion):
            if parametros[0].to_ast()['type'] == 'number':
                return parametros[0].to_ast()['valor']
            if parametros[0].to_ast()['type'] == 'infinite':
                return math.inf  
            if parametros[0].to_ast()['type'] == 'unary_operation':
                if parametros[0].to_ast()['op'] == 'RESTA':
                    return -parametros[0].to_ast()['valor']['valor']
                elif parametros[0].to_ast()['op'] == 'SUMA':
                    return parametros[0].to_ast()['valor']['valor']
                else:
                    print("Error: No se puede convertir a numero")
                    exit()              
            
        print("Error: No se puede convertir a numero")
        exit()
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
    elif name == 'Ln':
        return math.log(parametros[0])
    elif name == 'log':
        return math.ln(parametros[0],parametros[1])
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
    elif name == 'Date':
        return str(datetime.datetime.now().strftime("%a %d-%b-%Y"))
    elif name == 'Time':
        return str(datetime.datetime.now().strftime("%H:%M:%S %p"))
    elif name == 'Repeat':
        return str(parametros[0]) * int(parametros[1])
    elif name == 'Talk':
        if bool(parametros[1]):
            print(str(parametros[0]))
        engine = pyttsx3.init()
        engine.say(str(parametros[0]))
        engine.runAndWait()
    elif name == 'Ear':
        recognizer = speech_recognition.Recognizer()
        with speech_recognition.Microphone() as source:
            if(bool(parametros[0])):
                print("Escuchando...")
            audio = recognizer.listen(source)
            try:
                text = recognizer.recognize_google(audio, language='es-ES')
                return text
            except speech_recognition.UnknownValueError:
                return "No se entendió el audio"
            except speech_recognition.RequestError as e:
                return f"Error al conectar con el servicio de reconocimiento: {e}"
    elif name == 'Search':
        texto = str(parametros[0])
        
        #Buscar en wikipedia
        try:
            resultado = wikipedia.summary(texto,sentences=1)
            return resultado
        except wikipedia.exceptions.PageError:
            return "No se encontro ninguna pagina con este titulo"
        except wikipedia.exceptions.DisambiguationError as e:
            lista = ", ".join([x for x in e.options if x != ''])
            return f"El termino de busqueda es ambiguo. Por favor, especifica mas : {lista}"
        except Exception as e:
            return f"Ocurrio un error: {e}"
    elif name == 'system':
        os.system(str(parametros[0]))

methods = {
    'Reverse':0,
    'Equals':1,
}

def process_methods(name, id_, parametros):
    if name == 'Reverse':
        return str(id_)[::-1]
    elif name == 'Equals':
        return str(id_).count(str(parametros[0]))