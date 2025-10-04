# **Documentación Formal del Lenguaje Heza**

## **1. Introducción**

Heza es un lenguaje de programación especializado diseñado para la comunidad matemática y lógica. Su sintaxis incorpora notación matemática nativa, permitiendo una expresión más natural de conceptos matemáticos complejos.

**Características principales:**
- Notación matemática integrada
- Manipulación simbólica de expresiones
- Tipos de datos especializados para matemáticas
- Sintaxis declarativa y funcional
- Extensión de archivos: `.hz`

## **2. Elementos Básicos**

### **2.1 Comentarios**
**Qué hace:** Permite agregar anotaciones en el código que son ignoradas por el intérprete
**Sintaxis:** `@ texto del comentario`
**Ejemplo:**
```heza
@ Este es un comentario en Heza
@ Calculadora de números primos
```

### **2.2 Palabras Clave**
- `data` - Declaración de variables
- `trace` - Activa el historial de cambios
- `as` - Asigna alias a condiciones
- `end` - Termina bloques de código  
- `use` - Declara condiciones
- `play` - Reproduce bloques de código (bucles while)

### **2.3 Constantes Predefinidas**
- `TAB` - Tabulación
- `ESP` - Espacio en blanco
- `LINE` - Salto de línea
- `FALSE` - Valor booleano falso
- `TRUE` - Valor booleano verdadero
- `∅` - Valor nulo (NONE)
- `∞` - Infinito (INFINITE)
- `PI` - Constante π
- `E` - Constante e

## **3. Operadores**

### **3.1 Operadores Aritméticos**
- `+` - Suma
- `-` - Resta
- `*` - Multiplicación
- `%` - Módulo
- `^` - Potencia
- `/` - División

### **3.2 Operador de Asignación**
**Qué hace:** Asigna valores a variables
**Sintaxis:** `←`
**Ejemplo:**
```heza
data x ← 10
data resultado ← x + 5
```

### **3.3 Operadores Lógicos**
- `∧` - AND (conjunción)
- `¬` - NOT (negación)  
- `∨` - OR (disyunción)

### **3.4 Operadores de Relación**
- `=` - Igual
- `≠` - Diferente
- `>` - Mayor
- `<` - Menor
- `>=` - Mayor o igual
- `<=` - Menor o igual
- `∈` - Pertenencia (pertenece a)

## **4. Funciones Matemáticas**

### **4.1 Funciones Numéricas Integradas**
- `√` - Raíz cuadrada
- `∏` - Productoria
- `∑` - Sumatoria
- `∂` - Derivada
- `∫` - Integral
- `|x|` - Valor absoluto
- `!x` - Factorial
- `eval` - Evaluación de expresiones
- `lim` - Límites

### **4.2 Funciones Matemáticas Adicionales**
**Lista completa:** 
- `sign` - Función signo
- `root` - Raíz n-ésima
- `sqrt` - Raíz cuadrada
- `atanh, acosh, asinh` - Funciones hiperbólicas inversas
- `tanh, cosh, sinh` - Funciones hiperbólicas
- `arctan, arccos, arcsin` - Funciones trigonométricas inversas
- `citan, sec, cosec` - Funciones trigonométricas adicionales
- `exp, ln, log` - Funciones exponenciales y logarítmicas
- `tan, cos, sin` - Funciones trigonométricas básicas

## **5. Operadores Especiales**

- `→>` - UNIQUE (ejecuta un solo comando)
- `→` - THEN (entonces, para bloques)
- `⟹` - OUT (salida por consola)
- `⟸` - IN (entrada por consola)
- `∀` - FOREACH (para cada elemento)
- `∃` - EXIST (existe al menos un elemento)
- `:` - REFERENCE (referencia en comprehensions)
- `≔` - DEFINICIÓN (definición de funciones)

## **6. Tipos de Datos**

### **6.1 Tipos Básicos**
- **Numéricos:** `1212`, `1212.343` (enteros y decimales)
- **Booleanos:** `FALSE`, `TRUE` (valores lógicos)
- **Textos:** `"Hello"` (cadenas de caracteres)
- **Expresiones:** `'x^2'` (expresiones matemáticas sin evaluar)
- **Conjuntos:** `{4,7.4,"67",FALSE}` (colecciones de elementos)
- **Condiciones:** `use x>3` (expresiones condicionales)
- **Referencias:** `my_var` (referencias a variables)

## **7. Declaración de Variables**

### **7.1 Declaración Simple**
**Qué hace:** Declara una variable sin asignación inicial
**Sintaxis:** `data var`
**Ejemplo:**
```heza
data x
data y
```

### **7.2 Declaración con Asignación**
**Qué hace:** Declara y asigna valor a una variable
**Sintaxis:** `data var ← valor`
**Ejemplo:**
```heza
data nombre ← "Juan"
data edad ← 25
```

### **7.3 Declaración Múltiple**
**Qué hace:** Declara varias variables simultáneamente
**Sintaxis:** `data x,y,z`
**Ejemplo:**
```heza
data a,b,c
```

### **7.4 Declaración Múltiple con Asignación**
**Qué hace:** Declara y asigna valores a múltiples variables
**Sintaxis:** `data x ← 10, y, z ← 5`
**Ejemplo:**
```heza
data x ← 10, y, z ← 5
```

### **7.5 Declaración con Trace**
**Qué hace:** Activa el historial de cambios para variables
**Sintaxis:** `data trace var1,var2,...`
**Ejemplo:**
```heza
data trace contador, resultado
```

### **7.6 Reasignación de Variables**
**Qué hace:** Permite reasignar múltiples variables simultáneamente
**Sintaxis:** `a,b,c ← b,c,4`
**Ejemplo:**
```heza
data a ← 1, b ← 2, c ← 3
a,b,c ← b,c,4
⟹ a,b,c  @ Salida: 2, 3, 4
```

## **8. Entrada y Salida por Consola**

### **8.1 Entrada (INPUT)**
**Qué hace:** Lee valores desde la consola
**Sintaxis:** `⟸ var1,var2...`
**Ejemplo:**
```heza
data nombre, edad
⟸ nombre, edad
```

### **8.2 Salida (OUTPUT)**
**Qué hace:** Muestra valores en la consola
**Sintaxis:** `⟹ val1,val2...`
**Ejemplo:**
```heza
⟹ "Hola mundo"
⟹ "El resultado es:", resultado, LINE
```

## **9. Conjuntos**

### **9.1 Conjuntos por Extensión**
**Qué hace:** Crea un conjunto enumerando sus elementos
**Sintaxis:** `{elemento1, elemento2, ...}`
**Ejemplo:**
```heza
data arr ← {1,2,3,4,5,6,7,8,9,10}
```

### **9.2 Rangos**
**Qué hace:** Genera secuencias numéricas
**Sintaxis:** `[inicio..fin]` (incluyendo ambos extremos)
**Ejemplo:**
```heza
data arr ← [1..10]  @ {1,2,3,4,5,6,7,8,9,10}
```

### **9.3 Rangos con Paso**
**Qué hace:** Genera secuencias con incremento específico
**Sintaxis:** `[inicio..fin:paso]`
**Ejemplo:**
```heza
data arr ← [1..10:2]  @ {1,3,5,7,9}
```

### **9.4 Subconjuntos por Comprensión**
**Qué hace:** Filtra elementos de un conjunto según una condición
**Sintaxis:** `{x ∈ conjunto_padre : condicion}`
**Ejemplo:**
```heza
data conjunto_padre ← [1..10]
data subconjunto ← {x ∈ conjunto_padre : x%2=0}
@ Resultado: {2,4,6,8,10}
```

### **9.5 Transformación de Conjuntos (Mapeo)**
**Qué hace:** Aplica una función a todos los elementos de un conjunto
**Sintaxis:** `{f(x) | x ∈ conjunto_padre}`
**Ejemplo:**
```heza
data conjunto_padre ← {5,6,7}
data transformado ← {x*2 | x ∈ conjunto_padre}
@ Resultado: {10,12,14}
```

### **9.6 Mapeo con Múltiples Variables**
**Qué hace:** Combina elementos de múltiples conjuntos
**Sintaxis:** `{ {x,y} | x ∈ A, y ∈ B }`
**Ejemplo:**
```heza
data A ← [1..10]
data B ← [10..1]
data C ← { {x,y} | x ∈ A, y ∈ B }
@ Resultado: {{6, 5}, {7, 4}, {8, 3}, {9, 2}, {10, 1}}
```

### **9.7 Mapeo con Condición**
**Qué hace:** Combina elementos con filtrado
**Sintaxis:** `{ {x,y} | x ∈ A, y ∈ B : x>y }`
**Ejemplo:**
```heza
data A ← [1..10]
data B ← [10..1]
data C ← { {x,y} | x ∈ A, y ∈ B : x>y }
```

## **10. Cuantificadores como Verificadores**

### **10.1 Cuantificador Universal (∀)**
**Qué hace:** Verifica si todos los elementos cumplen una condición
**Sintaxis:** `∀ x ∈ set : condicion`
**Ejemplo:**
```heza
data conjunto ← {2,4,6,8}
data resultado ← ∀ x ∈ conjunto : x%2=0
@ Resultado: TRUE
```

### **10.2 Cuantificador Existencial (∃)**
**Qué hace:** Verifica si al menos un elemento cumple una condición
**Sintaxis:** `∃ x ∈ set : condicion`
**Ejemplo:**
```heza
data conjunto ← {1,3,5,8}
data resultado ← ∃ x ∈ conjunto : x%2=0
@ Resultado: TRUE
```

## **11. Expresiones Matemáticas**

### **11.1 Creación de Expresiones**
**Qué hace:** Crea expresiones matemáticas sin evaluar
**Sintaxis:** `'expresion_matematica'`
**Ejemplo:**
```heza
data funcion ← 'x+4'
data texto ← "x - 6"
data expre ← 'texto'  @ Referencia a variable texto
```

### **11.2 Concatenación de Expresiones**
**Qué hace:** Combina múltiples expresiones
**Sintaxis:** `'expresion1 operador expresion2'`
**Ejemplo:**
```heza
data e1 ← 'x - 45'
data e2 ← 'e1 / 2'
data e3 ← '5 * e1 - e2 * sin(x)'
```

### **11.3 Evaluación de Expresiones**
**Qué hace:** Evalúa expresiones sustituyendo variables
**Sintaxis:** `eval(expr)` o `eval(expr, var → valor)`
**Ejemplo:**
```heza
data expr ← 'x+5'
data x ← 5
⟹ eval(expr)  @ Resultado: 10 (como Expresión)

data expr2 ← 'x+5-y'
data x ← 6
⟹ eval(expr2, y → 3)  @ Resultado: x+2
```

### **11.4 Conversión a Número**
**Qué hace:** Convierte una expresión evaluada a tipo numérico
**Sintaxis:** `Num(expresion)`
**Ejemplo:**
```heza
data expr ← '5+3'
data numero ← Num(eval(expr))
```

## **12. Sumatorias y Productorias**

### **12.1 Sumatorias**
**Qué hace:** Calcula la suma de una operación sobre un conjunto
**Sintaxis:** `∑(x ∈ conjunto, operacion)`
**Ejemplo:**
```heza
⟹ ∑(x ∈ {1,2,4}, x^2)  @ Resultado: 21
⟹ ∑(x ∈ [0..10:5], x)  @ Resultado: 15
```

### **12.2 Productorias**
**Qué hace:** Calcula el producto de una operación sobre un conjunto
**Sintaxis:** `∏(x ∈ conjunto, operacion)`
**Ejemplo:**
```heza
⟹ ∏(x ∈ [1..5], x)      @ Resultado: 120
⟹ ∏(x ∈ {0,4,2}, x+1)  @ Resultado: 15
```

### **12.3 Uso con Expresiones**
**Qué hace:** Combina expresiones con sumatorias/productorias
**Sintaxis:** `∑(k ∈ conjunto, Num(eval(expresion, var → k)))`
**Ejemplo:**
```heza
data e ← 'x * 2'
⟹ ∑(k ∈ {0,5,10}, Num(eval(e, x → k)))  @ Resultado: 30
```

## **13. Recorrido de Conjuntos (Bucles)**

### **13.1 Bucle en Una Línea**
**Qué hace:** Ejecuta un comando para cada elemento
**Sintaxis:** `∀ var ∈ conjunto →> comando`
**Ejemplo:**
```heza
∀ var ∈ {"Hello"," Word"} →> ⟹ var
@ Salida: Hello Word
```

### **13.2 Bucle con Bloque Múltiple**
**Qué hace:** Ejecuta múltiples comandos para cada elemento
**Sintaxis:**
```heza
∀ var ∈ conjunto →
    comando1
    comando2
end:var
```
**Ejemplo:**
```heza
∀ x ∈ [1..10] →
    data aux ← ∑(k ∈ [1..x], k)
    ⟹ aux,LINE
end:x
```

### **13.3 Bucle con Múltiples Variables**
**Qué hace:** Itera sobre múltiples conjuntos simultáneamente
**Sintaxis:** `∀ x ∈ A, y ∈ B → ... end:x`
**Ejemplo:**
```heza
data A ← [1..10]
data B ← [10..1]
∀ x ∈ A, y ∈ B → 
    ⟹ x, " * ", y, " = ", x*y, LINE
end:x
```

## **14. Cálculo Diferencial e Integral**

### **14.1 Límites**
**Qué hace:** Calcula el límite de una expresión
**Sintaxis:** `lim(expr, var → valor)`
**Ejemplo:**
```heza
data funcion ← 'x^2'
data expresion ← '(eval(funcion, x → x+h) - funcion) / h'
⟹ lim(expresion, h → 0)  @ Resultado: 2*x
```

### **14.2 Derivadas**
**Qué hace:** Calcula la derivada de una expresión
**Sintaxis:** `∂(expr, var)`
**Ejemplo:**
```heza
⟹ ∂('x^2',x)  @ Resultado: 2*x
```

### **14.3 Integrales Indefinidas**
**Qué hace:** Calcula la integral indefinida
**Sintaxis:** `∫(expr, var)`
**Ejemplo:**
```heza
⟹ ∫('ln(x)/(2*x)',x)  @ Resultado: log(x)^2/4
```

### **14.4 Integrales Definidas**
**Qué hace:** Calcula la integral definida entre límites
**Sintaxis:** `∫(expr, var ∈ [limI..limS])`
**Ejemplo:**
```heza
⟹ ∫('3*x^2', x ∈ [0..2])  @ Resultado: 8
```

## **15. Funciones Definidas por el Usuario**

### **15.1 Definición de Funciones**
**Qué hace:** Crea funciones reutilizables
**Sintaxis:**
```heza
≔ (parametros) as nombre →
    bloque de código
    ↩ valor_retorno
end:nombre
```
**Ejemplo:**
```heza
≔ (nombre) as saludar →
    ⟹ "Hola, ",nombre,"!"
end:saludar

≔ (n) as sumatoria →
    ↩ ∑(k ∈ [1..n], k)
end:sumatoria
```

### **15.2 Llamada a Funciones**
**Qué hace:** Ejecuta una función definida
**Sintaxis:** `nombre_funcion(argumentos)`
**Ejemplo:**
```heza
saludar("Mundo")
⟹ sumatoria(4)  @ Resultado: 10
```

## **16. Acceso a Elementos por Índice**

### **16.1 Acceso a Conjuntos y Textos**
**Qué hace:** Accede a elementos específicos por posición
**Sintaxis:** `conjunto{indice}`
**Ejemplo:**
```heza
data mi_conjunto ← {10,20,30,40}
⟹ mi_conjunto{2}  @ Resultado: 20

data texto ← "Hola"
⟹ texto{1}  @ Resultado: "H"
```

## **17. Condicionales**

### **17.1 Declaración de Condiciones**
**Qué hace:** Crea condiciones reutilizables
**Sintaxis:** `use condicion as alias`
**Ejemplo:**
```heza
use edad>18 as mayor
```

### **17.2 Evaluación Simple de Condiciones**
**Qué hace:** Ejecuta código si se cumple una condición
**Sintaxis:**
```heza
condicion? →
    @ bloque si se cumple
end:condicion
```

### **17.3 Condicional con Else**
**Qué hace:** Ejecuta diferentes bloques según condición
**Sintaxis:**
```heza
condicion? →
    @ bloque si verdadero
¬ →
    @ bloque si falso
end:condicion
```
**Ejemplo:**
```heza
use edad>=18 as esMayor
data edad ⟸ edad

esMayor? →
    ⟹ "Es mayor de edad"
¬ →
    ⟹ "Es menor de edad"
end:esMayor
```

### **17.4 Evaluación Inmediata**
**Qué hace:** Declara y evalúa una condición inmediatamente
**Sintaxis:** `use condicion as alias? → ... end:alias`
**Ejemplo:**
```heza
data num ⟸ num
use num % 2 = 0 as esPar? →
    ⟹ "Es par"
¬ →
    ⟹ "Es impar"
end:esPar
```

## **18. Operador Ternario**

### **18.1 Sintaxis del Ternario**
**Qué hace:** Selecciona valores basados en condiciones
**Sintaxis:** `condicion? → valorVerdadero ¬ → valorFalso`
**Ejemplo:**
```heza
data a ← 6, b ← 8
use a>b as comparacion
⟹ comparacion? → a ¬ → b, " es mayor"

≔ (a,b) as max → 
    use a>b as cond
    ↩ cond? → a ¬ → b
end:max
```

## **19. Estructuras de Control Avanzadas**

### **19.1 Bucles For (simulados)**
**Qué hace:** Itera sobre un rango de valores
**Sintaxis:** `∀ i ∈ [limI..limS] → ... end:i`
**Ejemplo:**
```heza
∀ i ∈ [1..10] → 
    ⟹ "Iteración:", i
end:i
```

**En una línea:**
```heza
∀ i ∈ [1..10] →> ⟹ "Número:", i
```

### **19.2 Bucles While**
**Qué hace:** Ejecuta código mientras se cumple una condición
**Sintaxis:**
```heza
condicion? → play
    @ cuerpo del bucle
end:condicion
```
**Ejemplo:**
```heza
data contador ← 0
use contador < 5 as condicion? → play
    ⟹ "Contador:", contador
    data contador ← contador + 1
end:condicion
```

### **19.3 While con Else**
**Qué hace:** Bucle while con bloque alternativo si no se ejecuta
**Sintaxis:**
```heza
condicion? → play
    @ cuerpo del bucle
¬ →
    @ bloque si no se ejecuta
end:condicion
```

## **20. Sistema de Trace**

### **20.1 Activación de Trace**
**Qué hace:** Habilita el historial de cambios para variables
**Sintaxis:** `data trace var1,var2,...`
**Ejemplo:**
```heza
data trace contador, resultado
```

### **20.2 Acceso al Historial**
**Qué hace:** Obtiene el historial de cambios de una variable
**Sintaxis:** `trace:var`
**Ejemplo:**
```heza
data trace x
data x ← 1
data x ← 2
data x ← 3
⟹ trace:x  @ Muestra historial de cambios
```

## **21. Funciones Adicionales Integradas**

### **21.1 Funciones de Conversión**
- `Num(exp)` - Convierte expresión a número
- `Integer(str)` - Convierte texto a entero
- `String(num/conjunto)` - Convierte a texto

### **21.2 Funciones de Texto**
- `ToLowerCase(texto)` - Convierte a minúsculas
- `ToUpperCase(texto)` - Convierte a mayúsculas
- `Repeat(text, veces)` - Repite texto
- `Size(conjunto/texto)` - Obtiene tamaño/cantidad

### **21.3 Funciones de Sistema**
- `R(i,s)` - Número aleatorio entre i y s
- `Pressed("key")` - Verifica si tecla está presionada
- `Wait(milisegundos)` - Espera en milisegundos
- `Key()` - Espera presión de tecla
- `Date()` - Fecha actual
- `Time()` - Hora actual

### **21.4 Funciones Avanzadas**
- `Talk(text)` - Convierte texto a voz (español)
- `Ear()` - Escucha por micrófono y devuelve texto
- `Search(text)` - Busca en Wikipedia y devuelve texto
