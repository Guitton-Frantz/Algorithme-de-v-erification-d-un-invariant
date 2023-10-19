import sympy as sp


class TransitionSystem:
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
        pass

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
S = set(["s0", "s1", "s2", "s3", "s4", "s5"])
# Define the set of actions
Act = set(["a", "b"])
# Define the transition function
transitions = {"s0": {"a": "s1", "b": "s2"},
               "s1": {"a": "s3", "b": "s4"},
               "s2": {"a": "s4", "b": "s5"},
               "s3": {"a": "s3", "b": "s4"},
               "s4": {"a": "s4", "b": "s5"},
               "s5": {"a": "s5", "b": "s5"}}
# Define the set of initial states
I = set(["s0"])
# Define the set of propositions
Prop = set(["p", "q"])
# Define the labeling function
L = {"s0": set(["p"]),
     "s1": set(["p"]),
     "s2": set(["p"]),
     "s3": set(["q"]),
     "s4": set(["q"]),
     "s5": set(["q"])}
# Define the transition system
ST = TransitionSystem(S, Act, transitions, I, Prop, L)
# Define the invariant
Phi = sp.parse_expr("p & q")
# Verify the invariant
print(verify_invariant(ST, Phi))
