import string
from token2 import TOKEN

TABELA_DE_SIMBOLOS = [
    TOKEN('inicio', 'inicio', 'inicio'),
    TOKEN('varinicio', 'varinicio', 'varinicio'),
    TOKEN('varfim', 'varfim', 'varfim'),
    TOKEN('escreva', 'escreva', 'escreva'),
    TOKEN('leia', 'leia', 'leia'),
    TOKEN('se', 'se', 'se'),
    TOKEN('entao', 'entao', 'entao'),
    TOKEN('fimse', 'fimse', 'fimse'),
    TOKEN('fim', 'fim', 'fim'),
    TOKEN('inteiro', 'inteiro', 'inteiro'),
    TOKEN('literal', 'literal', 'literal'),
    TOKEN('real', 'real', 'real')
]


tabela_de_transicao = {
    0: {
        '(': 1,
        ')': 2,
        ';': 3,
        ',': 4,
        'EOF': 5,
        '+': 6,
        '-': 6,
        '*': 6,
        '/': 6,
        'letra': 7,
        '"': 8,
        '{': 10,
        '<': 12,
        '>': 14,
        '=': 15,
        'digito': 16,
        ' ': 0,
        '\n': 0,
        '\t': 0
    },
    1: {},
    2: {},
    3: {},
    4: {},
    5: {},
    6: {},
    7: {
        'letra': 7,
        'digito': 7,
        '_': 7
    },
    8: {
        'curinga': 8,
        '"': 9
    },
    9: {},
    10: {
        'curinga': 10,
        '}': 11
    },
    11: {},
    12: {
        '=': 15,
        '>': 15,
        '-': 13
    },
    13: {},
    14: {
        '=': 15
    },
    15: {},
    16: {
        'digito': 16,
        '.': 17,
        'E': 19,
        'e': 19
    },
    17: {
        'digito': 18
    },
    18: {
        'digito': 18,
        'E': 19,
        'e': 19
    },
    19: {
        'digito': 21,
        '+': 20,
        '-': 20
    },
    20: {
        'digito': 21
    },
    21: {
        'digito': 21
    }
}


estados_finais = {
    0: 'estado inicial',
    1: 'AB_P',
    2: 'FC_P',
    3: 'PT_V',
    4: 'VIR',
    5: 'EOF',
    6: 'OPA',
    7: 'id',
    9: 'Lit',
    11: 'Comentário',
    12: 'OPR',
    13: 'ATR',
    14: 'OPR',
    15: 'OPR',
    16: 'Num',
    18: 'Num',
    21: 'Num'
}


letras = list(string.ascii_letters)

digitos = list(string.digits)

delimitadores = [' ', '\n', '\t']

alfabeto = list(letras + digitos + delimitadores + [
    ',', ';', ':', '.', '!', '?', '\\', '*', '+', '-', '/', '(', ')', '{', '}',
    '[', ']', '<', '>', '=', "'", '"', '_'
])