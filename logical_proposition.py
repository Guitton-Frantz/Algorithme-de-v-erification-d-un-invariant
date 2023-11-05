class Proposition:
    def evaluate(self, context):
        pass

class Variable(Proposition):
    def __init__(self, name):
        self.name = name

    def evaluate(self, context):
        return context.get(self.name, False)

class Not(Proposition):
    def __init__(self, prop):
        self.prop = prop

    def evaluate(self, context):
        return not self.prop.evaluate(context)

class And(Proposition):
    def __init__(self, prop1, prop2):
        self.prop1 = prop1
        self.prop2 = prop2

    def evaluate(self, context):
        return self.prop1.evaluate(context) and self.prop2.evaluate(context)

class Or(Proposition):
    def __init__(self, prop1, prop2):
        self.prop1 = prop1
        self.prop2 = prop2

    def evaluate(self, context):
        print(context)
        return self.prop1.evaluate(context) or self.prop2.evaluate(context)
