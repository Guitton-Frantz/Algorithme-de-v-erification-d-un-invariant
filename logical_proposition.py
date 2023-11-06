class Proposition:
    def evaluate(self, context):
        pass

class Variable(Proposition):
    name : str

    def __init__(self, name):
        self.name = name

    def evaluate(self, label:list):
        return self.name in label

                

class Not(Proposition):
    prop : Proposition

    def __init__(self, prop):
        self.prop = prop

    def evaluate(self, label:set):
        return not self.prop.evaluate(label)

class And(Proposition):
    prop1 : Proposition
    prop2 : Proposition

    def __init__(self, prop1, prop2):
        self.prop1 = prop1
        self.prop2 = prop2

    def evaluate(self, label:set):
        return self.prop1.evaluate(label) and self.prop2.evaluate(label)

class Or(Proposition):
    prop1 : Proposition
    prop2 : Proposition

    def __init__(self, prop1, prop2):
        self.prop1 = prop1
        self.prop2 = prop2

    def evaluate(self, label:set):
        return self.prop1.evaluate(label) or self.prop2.evaluate(label)
