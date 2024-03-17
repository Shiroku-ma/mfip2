from term import Term
from expression import Expression as Expr
import math
import cmath
from fractions import Fraction as Fr

class IllegalEquationException(Exception):
    pass

class Solution:
    def __init__(self, body, is_imag=False):
        self.body = body
        self.is_imag = is_imag

    def __str__(self) -> str:
        parts = []
        if self.body[0] != 0:
            parts.append(str(self.body[0]))

        if not self.is_imag:
            if self.body[1] != 0 and self.body[2] != 0:
                a = str(self.body[1])
                b = str(self.body[2])
                if b == "1":
                    if self.body[0] == 0:
                        parts.append(a)
                    else:
                        parts.clear()
                        parts.append(str(Fr(self.body[0]) + Fr(a)))
                else:
                    if a == "1":
                        parts.append("√"+b)
                    elif a == "-1":
                        parts.append("-√"+b)
                    else:
                        parts.append(a+"√"+b)
        else:
            a = str(self.body[1])
            b = str(self.body[2])
            if b == "1":
                if a == "1":
                    parts.append("i")
                elif a == "-1":
                    parts.append("-i")
                else:
                    parts.append(a+"i")
            else:
                if a == "1":
                    parts.append("√"+b+"i")
                elif a == "-1":
                    parts.append("-√"+b+"i")
                else:
                    parts.append(a+"√"+b+"i")
        
        if len(parts) == 0:
            return "0"
        return " + ".join(parts)

class Equation:
    def __init__(self, left: Expr, right: Expr):
        self.left = left
        self.right = right

    def solve(self):
        expr: Expr = self.left - self.right
        expr.simplify()
        if expr.terms[0].exp == 1:
            [a,b] = expr.coefs()
            return [ Solution([Fr(-b,a), 0, 0]) ]
        elif expr.terms[0].exp == 2:
            [a,b,c] = expr.coefs()
            D = b**2-4*a*c
            if D > 0:
                [p,q] = self.__format_root(D)
                return [ Solution([Fr(-b,2*a), Fr(p,2*a), q]), Solution([Fr(-b,2*a), -Fr(p,2*a), q]) ]
            elif D == 0:
                return [ Solution([Fr(-b,2*a), 0, 0]) ]
            else:
                [p,q] = self.__format_root(-D)
                return [ Solution([Fr(-b,2*a), Fr(p,2*a), q], True), Solution([Fr(-b,2*a), -Fr(p,2*a), q], True) ]
            
        
    def __isRrational(self, n):
        return math.sqrt(abs(n)).is_integer()
    
    def __format_root(self, n):
        N = n
        primes = []
        while N % 2 == 0:
            primes.append(2)
            N /= 2
        i = 3
        while i <= math.sqrt(abs(N)):
            if N % i == 0:
                primes.append(i)
                N /= i
            else:
                i += 2
        if N != 1:
            primes.append(int(N))

        outside = 1
        inside = 1
        index = 0
        while index < len(primes):
            num = primes[index]
            count = primes.count(num)
            if count > 0 :
                if count % 2 == 0:
                    outside *= (num ** (count/2))
                else: 
                    outside *= (num ** ((count-1)/2))
                    inside *= num
            index += count
        
        return [int(outside), int(inside)]