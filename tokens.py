tokens = [

    #palabras clave
    ('DATA', r'data'),
    ('TRACE', r'trace'),
    ('LOOP', r'loop'),
    ('AS', r'as'),
    ('ENDLAP', r'endlap'),
    ('ENDNOW', r'endnow'),
    ('END', r'end'),
    ('BLOCK', r'block'),
    ('OUT', r'out'),
    ('INSERT', r'insert'),
    ('IN', r'in'),
    ('CORRUTINE', r'corrutine'),
    ('ATT', r'att'),
    ('BUG', r'bug'),
    ('DEFAULT', r'default'),

    ('AND',r'and'),
    ('OR',r'or'),
    ('NOT',r'not'),
    ('FALSE',r'false'),
    ('TRUE',r'true'),
    #Constantes
    ('CLS', r'CLS'),
    ('TAB', r'TAB'),
    ('ESP', r'ESP'),
    ('LINE', r'LINE'),
    
    #Patrones
    ('NUMBER', r'\d+(\.\d+)?'),
    ('STR', r'"([^"]*)"'),
    ('ID', r'[a-zA-Z_]\w*'),

    #\t \n ESP
    ('IGNORAR', r'\s'),

    #Comentarios
    ('COMENTARIO', r'@(.*)'),

    #Operadores
    ('DISTINTO', r'!='),
    ('COMPARACION',r'=='),
    ('MAYORE',r'>='),
    ('MENORE',r'<='),
    ('ASIGNACION', r'='),
    ('PIPE', r'>>'),
    ('BACK', r'<\*>'),
    ('ARROW', r'->'),
    ('DOUBLEQ', r'\?\?'),
    ('Q', r'\?'),
    ('DOUBLEEXC', r'!!'),
    ('EXC', r'!'),
    ('MENOR',r'<'),
    ('MAYOR',r'>'),
    ('SUMA',r'\+'),
    ('RESTA',r'-'),
    ('MULTIPLICACION',r'\*'),
    ('DIVISION',r'/'),
    ('MOD',r'%'),
    ('POW',r'\^'),
    ('PUNTO', r'\.'),
    ('COMA', r','),
    ('REFERENCE', r':'),
    ('OPENP', r'\('),
    ('CLOSEP', r'\)'),
    ('DOLLAR', r'\$')
]

ExpresionValues = ['ID','STR','NUMBER','ESP','LINE','TAB','FALSE','TRUE','OPENP','RESTA','SUMA','NOT','TRACE']