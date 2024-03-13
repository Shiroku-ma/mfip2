from fractions import Fraction

class Term:
    def __init__(self, coef: Fraction, exp):
        self.coef: Fraction = coef
        self.exp = exp
    
    def __mul__(self, other):
        return self.__class__(self.coef * other.coef, self.exp + other.exp)
    
    def __truediv__(self, other):
        return self.__class__(self.coef / other.coef, self.exp - other.exp)
    
    def __str__(self):
        coef =str(self.coef)
        exp = str(self.exp)
        if coef == "0":
            return ""
        if exp == "0":
            return coef
        if exp == "1":
            if coef == "1":
                return "x"
            elif coef == "-1":
                return "-x"
            return coef + "x"
        if coef == "1":
            coef = ""
        elif coef == "-1":
            coef = "-"
        
        return coef + "x^" + exp
        
    