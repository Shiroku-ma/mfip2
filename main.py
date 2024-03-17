from fractions import Fraction
from term import Term
from expression import Expression as Expr
from equation import Equation

pos = 0

char_dct = {
    "1", "2", "3", "4", "5",
    "6", "7", "8", "9", "0",
    "x", "-" # このマイナスは減算のマイナスではなく負を表すためのマイナス
}

# 掛け算の記号 * を省略する際に括弧の前に置かれる文字
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
    v = element(line)
    while pos < len(line) and (line[pos] == "*" or line[pos] == "/" or (line[pos-1] in special and line[pos] == "(")):
        op = line[pos]
        pos += 1
        if op == "*":
            v = v * element(line)
        elif op == "/":
            v = v / element(line)
        elif op == "(":
            pos -= 1
            v = v * element(line)
    return v

def element(line):
    global pos
    v = factor(line)
    while pos < len(line) and line[pos] == "^":
        pos += 1
        v = v ** element(line)
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

if __name__ == "__main__":
    _line = input("> ")
    line = _line.replace(" ", "")
    eq = line.split("=")
    try:
        pos = 0
        vl = eval2(eq[0])
        if pos != len(eq[0]):
            raise IllegalExpressionException()
        pos = 0
        vr = eval2(eq[1])
        if pos != len(eq[1]):
            raise IllegalExpressionException()
        equation = Equation(vl, vr)
        ans = equation.solve()
        if len(ans) == 1:
            print(ans[0])
        else:
            print(ans[0])
            print(ans[1])
    except:
        import traceback
        traceback.print_exc()


# 1/2x => 1/(2x)
        