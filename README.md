# Heza: Un Lenguaje para la Computación Matemática y Simbólica

**Introdución**

Heza es un lenguaje interpretado de 3 fases diseñado para entender y procesar la notación matemática y lógica de alto nivel y asi simplificar el proceso de traducción centralizando el funcionamiento del lenguaje, está capacitado con motores del cálculo numérico y simbólico que facilitan la comprensión. Su fiel notación matemática lo hace perfecto para estudiantes que cursan matemáticas y lógica ya que la curva de aprendizaje es muy baja, logrando así una mayor concentración el área de estudio y reduciendo el tiempo lleva aprender la sintáxis del lenguaje.

**Tecnologías utilizadas**

Este proyecto está realizado 100% en python, con integración de la biblioteca Sympy como motor de cálculo simbólico, cabe destacar que python ya es un lenguaje interpretado por lo cual es tiempo de ejecución de un archivo `Heza` es notoriamente mas lento que los lenguajes compilados como C++

**Recomendaciones**

Dado que el proyecto no está totalmente optimizado, no es recomendable ejecutar código extremadamente pesado con fines comerciales o de investigación profunda ya que se podría quedar esperando por días e incluso semanas. Lo que recomiendo es utilizar éste lenguaje con fines de práctica educativa principalmente en el área de lógica, con esta herramienta es mas fácil visualizar y comprobar los resultados de un ejercicio que en una hoja de papel

**Conclusion**

Heza es un lenguaje de nicho que llena un vacío importante en el ecosistema de la programación. Al priorizar la elegancia matemática y la precisión sobre el rendimiento, ofrece una experiencia de programación única para quienes trabajan con la ciencia y el cálculo. Su capacidad para traducir conceptos abstractos en código funcional lo convierte en un lenguaje prometedor para el futuro de la educación y la computación científica.

## Sintaxis
**Palabras clave**
- data     (para declarar variables)
- trace    (activa y extrae el trazado de variables)
- as       (asigna un alias a un bloque de codigo de forma explicita)
- end      (termina un bloque de codigo especifico)

**Operadores de asignación**
- ←        (Asigna valores a variables)
- ≔        (Define funciones)

**Operadores aritméticos**
- (+)        (suma)
- (-)        (resta)
- (*)        (multiplicacion)
- (/)        (division)
- (%)        (mod)
- (^)        (potencia)

**Operadores de reacion**
- (=)        (igual)
- (≠)        (diferente)
- (>)        (mayor que)
- (<)        (menor que)
- (>=)       (mayor igual)
- (<=)       (menor igual)
- (∈)        (pertenece)

**Operadores de flujo**
- ⟹  (Salida por consola)
- ⟸  (entrada por consola)
- ↩  (retorno en funciones)
- →  (entonces)
- →> (unico, para bloque de codigo de una sola linea)

**Operadores logicos**
- ∧ (AND)
- ¬ (NOT)
- ∨ (OR)

**Operadores Especiales**
- ∀ (Cuantificador universal)
- ∃ (Cuantificador existensial)
- : (Referencia)
- | (Barra)
- ! (Exc)
- √ (Raiz cuadrada)
- ∏ (Productoria)
- ∑ (Sumatoria)
- ∂ (derivada)
- ∫ (integral)

**Tipo de datos**
- Numericos: 4 - 6.76
- Texto: "Hello wordl!"
- Booleanos: FALSE - TRUE
- Expresion: 'x^2 - 4y / 3'
- Conjuntos: {4,65,21}
- None: ∅
- Infinito: ∞

**Constantes**
- PI (numerico)
- E (numerico)
- FALSE (booleano)
- TRUE (booleano)
- ESP (Texto, espacio en blanco)
- LINE (Texto, salto de linea)
- TAB (Texto, salto de tabulador)
- ∅ (None)
∞ (Infinito)

## Semantica
**Declaracion de variables**
* Declaracion Simple:
  
  `data var`
* Declaracion con asignacion:
  
  `data var ← valor`
* Declaracion multiple:
  
  `data x,y,z`
* Declaracion multiple con asignacion:
  
  `data x ← 5, y ← TRUE, z ← "Hello"`

* Declaracion con trace:
  
  `data trace var` (con todas sus variantes)

**Conjuntos**
* Por extension {}:
  
  `data set ← {1,2,3,4,5}`

* De Rango []:
  
  `data set ← [1..10]` ( {1,2,3,4,5,6,7,8,9,10} )

* Rango con paso [:]:
  
  `data set ← [0..100:10]` (los numeros de 10 en 10 desde el 0 hasta el 100)

* Subconjunto por compresion (filtro):
  
  sintaxis  `data set ← {x ∈ conjunto_padre: condicion}`

   ejemplo

  `data conjunto_padre ← [1..10]`
  
   `data subconjunto ← {x ∈ conjunto_padre: x % 2 = 0}` (Se lee como los x pertenecientes a conjunto_padre tales que x % 2 = 0)

* Transformacion de conjuntos (mapeo):
  
  sintaxis  `data set ← { F(x) | x ∈ conjunto}`

   ejemplo

  `data conjunto ← {2,3,4}`
  
   `data conjunto_x2 ← { x*2 | x ∈ conjunto}` ( {4,6,8} )
