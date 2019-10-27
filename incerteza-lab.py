import sympy as sp
import math
from sympy.printing import pprint
from sympy.parsing.sympy_parser import parse_expr, standard_transformations

def parse(s):
    return parse_expr(s, transformations=standard_transformations)

def incerteza_absoluta(f: sp.Expr) -> sp.Expr:
    uf = 0
    udict = {}

    for s in f.free_symbols:
        udict[s] = sp.Symbol('u' + str(s))
        uf += udict[s] ** 2 * sp.simplify(f.diff(s) ** 2)
    uf = sp.sqrt(uf)
    return uf

def incerteza_relativa(f: sp.Expr, v: sp.Symbol) -> sp.Expr:
    uf = 0
    udict = {}

    for s in f.free_symbols:
        udict[s] = sp.Symbol('u' + str(s))
        df = sp.simplify(f.diff(s) ** 2 / f ** 2)
        uf += udict[s] ** 2 * df
    uf = v * sp.sqrt(uf)
    return uf

key = ""
while key != "sair":
    print("""\n
Qual o símbolo da grandeza da qual você quer achar a incerteza?

detalhe: não use 'I' ou 'i' pois gera problemas com números complexos

exemplo: Vlim

""")
    simb = sp.symbols(input())

    print("""
Qual a fórmula para essa grandeza?

escreva como você escreveria uma expressão em Python.
insira quantos símbolos extras forem necessários, mas não use I ou i.

Algumas funções são conhecidas:
 - exponenciação: use ** em vez de ^
 - multiplicação: sempre escreva explicitamente 2*a, nunca 2a
 - algumas funções suportadas: cos(x), sin(x), ln(x), log(x), etc.
 
exemplo: 2*(ρ - ρl)*g / (9*a)

""")
    
    ok = False
    while not ok:
        print("escreva a fórmula:\n")
        try:
            form = parse(input())
            print("\nSua expressão:")
            pprint(form)
            if input("\nParece OK? (s/n)\n") == 's':
                ok = True
        except SyntaxError:
            print("Há um problema com a fórmula... tente de novo")
    
    print()
    print(f"""Como você quer a formatação da incerteza?
    (r): relativa (padrão) - a resposta sai na forma '{simb} * raiz de alguma coisa'
    (a): absoluta - a resposta sai na forma 'raiz de alguma coisa'""")
    if input() == 'a':
        inc = incerteza_absoluta(form)
    else:
        inc = incerteza_relativa(form, simb)

    print()
    print(f"A expressão da incerteza para {simb} é:")
    pprint(inc)
