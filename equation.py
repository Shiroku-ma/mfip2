from term import Term
from expression import Expression as Expr
import math
import cmath
from fractions import Fraction as F

class IllegalEquationException(Exception):
    pass

class Solution:
    def __init__(self, re_ra=F(0), re_ir=[F(0),0], im_ra=F(0), im_ir=[F(0),0]):
        self.re_ra = re_ra
        self.re_ir = re_ir
        self.im_ra = im_ra
        self.im_ir = im_ir
    
    def __str__(self) -> str:
        result = ""
        if self.re_ra != 0:
            c = self.re_ra
            if c == 1:
                c = ""
            elif c == -1:
                c = "-"
            result += str(c)
        if self.re_ir[0] != 0 and self.re_ir[1] != 0:
            if result != "":
                result += "+"
            outside = self.re_ir[0]
            inside = self.re_ir[1]
            if inside == 1:
                if outside == 1:
                    result += "1"
                else:
                    result += str(outside)
            elif outside == 1:
                result += "√" + str(inside)
            else:
                result += str(outside) + "√" + str(inside)
        if self.im_ra != 0:
            if result != "":
                result += "+"
            c = self.im_ra
            if c == 1:
                c = ""
            elif c == -1:
                c = "-"

            result += str(c) + "i"
        if self.im_ir[0] != 0 and self.im_ir[1] != 0:
            if result != "":
                result += "+"
            outside = self.im_ir[0]
            inside = self.im_ir[1]
            if inside == 1:
                if outside == 1:
                    result += "i"
                else:
                    result += str(outside) + "i"
            elif outside == 1:
                result += "√" + str(inside) + "i"
            else:
                result += str(outside) + "√" + str(inside) + "i"
        if result == "":
            result = 0

        return result

class Equation:
    def __init__(self, left: Expr, right: Expr):
        self.left = left
        self.right = right

    def solve(self):
        expr: Expr = self.left - self.right
        expr.simplify()
        if expr.terms[0].exp == 1:
            [a,b] = expr.coefs()
            return [Solution(F(-b, a))]
        elif expr.terms[0].exp == 2:
            [a,b,c] = expr.coefs()
            D = b**2-4*a*c
            x1 = []
            x2 = []
            print(a,b,c)

            if D == 0:
                return [Solution(F(-b,2*a))]
            if self.__isRrational(D):
                d2 = math.floor(math.sqrt(abs(D)))
                if D < 0:
                    x1 = Solution(F(-b,2*a), [F(0),0], F(d2, 2*a), [F(0),0])
                    x2 = Solution(F(-b,2*a), [F(0),0], -F(d2, 2*a), [F(0),0])
                else:
                    x1 = Solution(F(-b+d2,2*a))
                    x2 = Solution(F(-b-d2,2*a))
            else:
                root = self.__format_root(D)
                if D < 0:
                    x1 = Solution(F(-b,2*a), [F(0),0], [F(0),0], [F(root[0], 2*a), root[1]])
                    x2 = Solution(F(-b,2*a), [F(0),0], [F(0),0], [-F(root[0], 2*a), root[1]])
                else:
                    x1 = Solution(F(-b,2*a), [F(root[0], 2*a), root[1]])
                    x2 = Solution(F(-b,2*a), [-F(root[0], 2*a), root[1]])
            return [x1, x2]
        
    def __isRrational(self, n):
        return math.sqrt(abs(n)).is_integer()
    
    def __format_root(self, n):
        N = abs(n)
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