tokens = [

    #palabras clave
    ('DATA', r'data'),
    ('TRACE', r'trace'),
    ('AS', r'as'),
    ('END', r'end'),
    ('USE', r'use'),
    ('PLAY', r'play'),
    #Constantes
    ('FALSE',r'false'),
    ('TRUE',r'true'),
    ('TAB', r'TAB'),
    ('ESP', r'ESP'),
    ('LINE', r'LINE'),

    #Signos
    ('DEF', r'≔'),
    ('ASIGNACION', r'←'),
    ('UNIQUE', r'→>'),
    ('THEN', r'→'),
    ('OUT', r'⟹'),
    ('INPUT', r'⟸'),
    ('IN', r'∈'),
    ('RETURN', r'↩'),
    ('AND', r'∧'),
    ('OR', r'∨'),
    ('NOT', r'¬'),
    ('SCOPE', r'◎'),
    ('SQRT', r'√'),
    ('NONE', r'∅'),
    ('FOREACH', r'∀'),
    ('EXIST', r'∃'),
    ('SUBJET', r'⊂'),
    ('DIFFERENT', r'≠'),
    ('SUMMATION', r'∑'),
    ('PRODUCTION', r'∏'),
    ('INFINITE', r'∞'),
    ('DERIVATIVE', r'∂'),
    ('INTEGRAL', r'∫'),
    
    #Patrones
    ('NUMBER', r'\d+(\.\d+)?'),
    ('STR', r'"([^"]*)"'),
    ('EXPRESION', r"'([^']*)'"),
    ('ID', r'[a-zA-Z_]\w*'),

    #\t \n ESP
    ('IGNORAR', r'\s'),

    #Comentarios
    ('COMENTARIO', r'@(.*)'),

    #Operadores
    ('COMPARACION', r'='),
    ('MAYORE',r'>='),
    ('MENORE',r'<='),
    ('PIPE', r'>>'),
    ('BACK', r'<\*>'),
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
    ('OPENC', r'\['),
    ('CLOSEC', r'\]'),
    ('OPENL', r'\{'),
    ('CLOSEL', r'\}'),
    ('DOLLAR', r'\$'),
    ('BARRA', r'\|') 
]

ExpresionValues = ['ID','STR','NUMBER','ESP','LINE','TAB','FALSE','TRUE','OPENP','OPENC','RESTA','SUMA','NOT','TRACE','SQRT','SUMMATION','NONE','BARRA','EXC','OPENL','FOREACH','EXIST','INFINITE','PRODUCTION','EXPRESION','DERIVATIVE','INTEGRAL']

ExpresionList = ['OPENP','ID','OPENL','OPENC','STR']

ExpresionExpr = ['EXPRESION', 'ID', 'DERIVATIVE', 'INTEGRAL']