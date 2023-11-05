import logical_proposition as lp

class State:
    state: tuple[str]
    def __init__(self, state):
        self.state = state

    def __eq__(self, other):
        return self.state == other.state
    
    def __hash__(self):
        return hash(self)
    


class TransitionSystem:
    S: set[State]
    Act: set
    transitions: dict
    I: set
    Prop: set
    L: dict
    def __init__(self, S, Act, transitions, I, Prop, L):
        self.S = S  # Set of states
        self.Act = Act  # Set of actions
        self.transitions = transitions  # Transition function
        self.I = I  # Set of initial states
        self.Prop = Prop  # Set of propositions
        self.L = L  # Labeling function

    def is_satisfied(self, s, proposition):
        # Implement the logic to evaluate the proposition for the state s
        return proposition.evaluate(self.L.get(s))

    def Post(self, s):
        # Implement the logic to compute the Post(s, act)
        # return the first state accessible from s 
        trans = self.transitions.get(s)
        return next(iter(trans))
        

# Define the verify_invariant function
def verify_invariant(ST : TransitionSystem, Phi):
    R = set() # Set of accessible states
    U = [] # Stack of states
    b = True # All states in R satisfy Phi
    while (ST.I - R) != (set() and b):
        s = (ST.I - R).pop() # Choose an arbitrary initial state not in R
        visiter(s, ST, Phi, R, U, b) # Call the scanning procedure
    if b:
        return "OUI" # ST always satisfies Phi
    else:
        return ("NON", U) # U provides a counterexample

# Define the visiter function
def visiter(s, ST, Phi, R, U, b):
    U: list = [] # Stack of states
    U.append(s) # Add s to the stack
    R.add(s) # Mark s as accessible
    while U == [] or not b:
        print(U)
        s_prime = U[-1] # s_prime is the top element of the stack ----to verify----
        #TODO check if the next of s' is in R
        if ST.Post(s_prime) not in R:
            U.pop() # Remove the top element of the stack
            b = b and ST.is_satisfied(s_prime, Phi) # Check the validity of Phi in s_prime
        else:
            s_double_prime = (ST.Post(s_prime) - R)# Choose an element in Post(s') \ R
            U.append(s_double_prime)
            R.add(s_double_prime) # s_double_prime is a new accessible state


# Test the algorithm
# Define the set of states
state0 = ("nc1", "nc2", "y=1")
state1 = ("p1", "nc2", "y=1")
state4 = ("c1", "nc2", "y=0")
state2 = ("nc1", "p2", "y=1")
state5 = ("nc1", "c2", "y=0")
state3 = ("p1", "p2", "y=1")
state6 = ("c1", "p2", "y=0")
state7 = ("p1", "c2", "y=0")

S = set({state0, state1, state2, state3, state4, state5, state6, state7})

# Define the set of actions
Act = set(["y <- y+1", "(y > 0): y <- y-1", "null"])
# Define the transition function
transitions = {
    state0: [state1, state2],
    state1: [state3, state4],
    state2: [state3, state5],
    state3: [state6, state7],
    state4: [state0, state6],
    state5: [state0, state7],
    state6: [state2],
    state7: [state1],
}
# Define the set of initial states
I = set(state0)
# Define the set of propositions
Prop = set(["c1", "c2"])
# Define the labeling function
L = {
    state0: {"nc1", "nc2"},
    state1: {"p1", "nc2"},
    state2: {"nc1", "p2"},
    state3: {"c1", "c2"},
    state4: {"c1", "nc2"},
    state5: {"nc1", "c2"},
    state6: {"c1","p2"},
    state7: {"p1", "c2"},
}

# Define the transition system
ST = TransitionSystem(S, Act, transitions, I, Prop, L)

# Define the invariant
Phi = lp.Or(lp.Not(lp.Variable("c1")), lp.Not(lp.Variable("c2")))

# Verify the invariant
print(verify_invariant(ST, Phi))
