from fractions import Fraction
from term import Term
from expression import Expression as Expr

pos = 0

char_dct = {
    "1", "2", "3", "4", "5",
    "6", "7", "8", "9", "0",
    "x", "-" # このマイナスは減算のマイナスではなく負を表すためのマイナス
}

special = {
    "1", "2", "3", "4", "5",
    "6", "7", "8", "9", "0",
    "x", ")"
}

class IllegalExpressionException(Exception):
    pass

def eval2(line):
    global pos
    pos = 0
    return expr(line)

def expr(line):
    global pos
    v = term(line)
    while pos < len(line) and (line[pos] == "+" or line[pos] == "-"):
        op = line[pos]
        pos += 1
        if op == "+":
            v = v + term(line)
        elif op == "-":
            v = v - term(line)
    return v

def term(line):
    global pos
    v = factor(line)
    while pos < len(line) and (line[pos] == "*" or line[pos] == "/" or (line[pos-1] in special and line[pos] == "(")):
        op = line[pos]
        pos += 1
        if op == "*":
            v = v * factor(line)
        elif op == "/":
            v = v / factor(line)
        elif op == "(":
            pos -= 1
            v = v * factor(line)
    return v

def factor(line):
    global pos
    v = None
    if line[pos] == "(":
        pos += 1
        v = expr(line)
        if pos == len(line) or line[pos] != ")":
            raise IllegalExpressionException()
        pos += 1
    else:
        v = number(line)
    return v

def number(line):
    global pos
    tmp = ""
    exp = 0
    while pos < len(line) and line[pos] in char_dct:
        if line[pos] == "-" and pos > 0 and not line[pos-1] in ["*", "/", "("]:
            break
        if line[pos] == "x":
            exp = 1
        else:
            tmp += line[pos]
        pos += 1

    if tmp == "":
        tmp = "1"
    elif tmp == "-":
        tmp = "-1"
    return Expr(Term(Fraction(tmp), exp))

# 同類項でまとめる
def simplify(expr: Expr):
    simplified_terms =[]
    exps = []
    for term in expr.terms: # 指数を登録(重複なし)
        if not term.exp in exps:
            exps.append(term.exp)
    for exp in exps:
        value = Fraction(0)
        for term in [_term for _term in expr.terms if _term.exp == exp]:
            value += term.coef
        simplified = Term(value, exp)
        simplified_terms.append(simplified)
    
    result = Expr(Term(1,1))
    result.terms = sorted(simplified_terms, key=lambda term: term.exp, reverse=True)
    return result
    

if __name__ == "__main__":
    _line = input("> ")
    line = _line.replace(" ", "")
    try:
        pos = 0
        v = eval2(line)
        if pos != len(line):
            raise IllegalExpressionException()
        r = simplify(v)
        print(r)
    except:
        import traceback
        traceback.print_exc()

# 1/2x => 1/(2x)
        