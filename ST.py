import sympy as sp


class TransitionSystem:
    S: set
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
        # You can use SymPy or implement your own logic here.
        sp.eval_expr(proposition, self.L.get(s))

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
S = [
    ["nc1", "nc2", "y=1"],
    ["p1", "nc2", "y=1"],
    ["c1", "nc2", "y=0"],
    ["nc1", "p2", "y=1"],
    ["nc1", "c2", "y=0"],
    ["p1", "p2", "y=1"],
    ["c1", "p2", "y=0"],
    ["p1", "c2", "y=0"],
]
# Define the set of actions
Act = set(["y <- y+1", "(y > 0): y <- y-1", "null"])
# Define the transition function
transitions = {["nc1", "nc2", "y=1"]:{["p1", "nc2", "y=1"],["nc1", "p2", "y=1"]},
                ["p1", "nc2", "y=1"]:{["p1", "p2", "y=1"],["c1", "nc2", "y=0"]},
                ["c1", "nc2", "y=0"]:{["c1", "p2", "y=0"],["nc1", "nc2", "y=1"]},
                ["nc1", "p2", "y=1"]:{["p1", "p2", "y=1"],["nc1", "c2", "y=0"]},
                ["nc1", "c2", "y=0"]:{["p1", "c2", "y=0"],["nc1", "nc2", "y=1"]},
                ["p1", "p2", "y=1"]:{["c1", "p2", "y=0"],["p1", "c2", "y=0"] },
                ["c1", "p2", "y=0"]:{["nc1", "p2", "y=1"]},
                ["p1", "c2", "y=0"]:{["p1", "nc2", "y=1"]},
               }
# Define the set of initial states
I = set([["nc1", "nc2", "y=1"]])
# Define the set of propositions
Prop = set(["c1", "c2"])
# Define the labeling function
L = {["nc1", "nc2", "y=1"]:set(["not c1", "not c2"]),}

# Define the transition system
ST = TransitionSystem(S, Act, transitions, I, Prop, L)

# Define the invariant
Phi = sp.parse_expr("(not crit1 or not crit2)")

# Verify the invariant
print(verify_invariant(ST, Phi))
