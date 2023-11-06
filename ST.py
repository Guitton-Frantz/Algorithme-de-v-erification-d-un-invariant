from logical_proposition import Proposition

class State:
    name: str
    def __init__(self, name:str):
        self.name = name

    def __hash__(self):
        return hash(self.name)

class TransitionSystem:
    s: set[State]
    Act: set[str]
    transitions: dict[State, list[State]]
    i: set[State]
    Prop: set[str]
    l: dict

    def __init__(self, s, Act, transitions, i, Prop, l):
        self.s = s  # Set of states
        self.Act = Act  # Set of actions
        self.transitions = transitions  # Transition function
        self.i = i  # Set of initial states
        self.Prop = Prop  # Set of propositions
        self.l = l  # Labeling function

    # Implement the logic to evaluate the proposition for the state s
    def is_satisfied(self, state:State, proposition:Proposition):
        return proposition.evaluate(self.l.get(state))

    # Return the states accessible from state
    def Post(self, state:State):
        return self.transitions.get(state)
        
class verify:
    r:set[State] # Set of accessible states
    u:list[State] # Stack of states
    b:bool # All states in R satisfy Phi

    def __init__(self):
        self.r = set()
        self.u = list()
        self.b = True

    # Define the verify_invariant function
    def verify_invariant(self, ST : TransitionSystem, Phi):
        while (ST.i - self.r) != set() and self.b:
            state = (ST.i - self.r).pop() # Choose an arbitrary initial state not in R
            self.visiter(state, ST, Phi, self.r, self.u, self.b) # Call the scanning procedure
        if self.b:
            return "OUI" # ST always satisfies Phi
        else:
            # Return a counterexample with the list of states in U
            return ("NON", self.u)
        
    # Define the visiter function
    def visiter(self, state, ST, Phi, r, u, b):
        self.u.append(state) # Add s to the stack
        self.r.add(state) # Mark s as accessible
        while len(self.u) > 0 and self.b:
            s_prime = self.u[len(self.u)-1] 
            # verify for each post(s') if it is in R
            present = True
            for s_prime_prime in ST.Post(s_prime):
                if s_prime_prime not in self.r:
                    present = False
                    break
            if present:
                self.u.pop() # Remove the top element of the stack
                self.b = (self.b and ST.is_satisfied(s_prime, Phi)) # Check the validity of Phi in s_prime
            else:
                # Choose an element in Post(s') that is not in R with a loop
                for s_prime_prime in ST.Post(s_prime):
                    if s_prime_prime not in self.r:
                        s_double_prime = s_prime_prime
                        break
                u.append(s_double_prime)
                r.add(s_double_prime) # s_double_prime is a new accessible state