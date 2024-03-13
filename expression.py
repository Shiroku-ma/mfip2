from term import Term
from fractions import Fraction

class IllegalExpressionException(Exception):
    pass

class Expression:
    def __init__(self, term: Term):
        if term == None:
            self.terms = [Term(1,1)]
        else:
            self.terms = [term]

    def __add__(self, other):
        self.terms += other.terms
        return self
    
    def __sub__(self, other):
        minus_other = [ Term(term.coef * -1, term.exp) for term in other.terms]
        self.terms += minus_other
        return self
    
    def __mul__(self, other):
        result = Expression(None)
        result.terms = []
        for s in self.terms:
            for o in other.terms:
                result.terms.append(s * o)
        return result
    
    def __truediv__(self, other):
        result = Expression(None)
        result.terms = []
        for s in self.terms:
            for o in other.terms:
                result.terms.append(s / o)
        return result
    
    def __pow__(self, other):
        other.simplify()
        if other.isInt():
            result = Expression(Term(1,0)) # 1 (0乗は１)
            for i in range(int(other.terms[0].coef)):
                result = result * self
            return result
        else:
            print("Index must be a number.")
            raise IllegalExpressionException()
    
    def __str__(self):
        terms = [term for term in self.terms if term.coef != 0]
        result = str(terms.pop(0))
        for term in terms:
            if term.coef > 0:
                result += " + " + str(term)
            else:
                result += " " + str(term)
            
        return result
    
    def isInt(self):
        if len(self.terms) == 1 and self.terms[0].exp == 0 and self.terms[0].coef.is_integer():
            return True
        return False

    def simplify(self):
        simplified_terms =[]
        exps = []
        for term in self.terms: # 指数を登録(重複なし)
            if not term.exp in exps:
                exps.append(term.exp)
        for exp in exps:
            value = Fraction(0)
            for term in [_term for _term in self.terms if _term.exp == exp]:
                value += term.coef
            simplified = Term(value, exp)
            simplified_terms.append(simplified)
        
        self.terms = sorted(simplified_terms, key=lambda term: term.exp, reverse=True)