from term import Term

class Expression:
    def __init__(self, term: Term):
        self.terms = [term]

    def __add__(self, other):
        self.terms += other.terms
        return self
    
    def __sub__(self, other):
        minus_other = [ Term(term.coef * -1, term.exp) for term in other.terms]
        self.terms += minus_other
        return self
    
    def __mul__(self, other):
        result = Expression(Term(1,1))
        result.terms = []
        for s in self.terms:
            for o in other.terms:
                result.terms.append(s * o)
        return result
    
    def __truediv__(self, other):
        result = Expression(Term(1,1))
        result.terms = []
        for s in self.terms:
            for o in other.terms:
                result.terms.append(s / o)
        return result
    
    def __str__(self):
        terms = [term for term in self.terms if term.coef != 0]
        result = str(terms.pop(0))
        for term in terms:
            if term.coef > 0:
                result += " + " + str(term)
            else:
                result += " " + str(term)
            
        return result