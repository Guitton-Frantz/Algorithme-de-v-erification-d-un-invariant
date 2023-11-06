from ST import State, TransitionSystem
from logical_proposition import Not, Or, Variable
from ST import verify

# --------Test the algorithm--------

# Define the set of states

state0 = State("0")
state1 = State("1")
state2 = State("2")
state3 = State("3")
state4 = State("4")
state5 = State("5")
state6 = State("6")
state7 = State("7")

s = set({state0, state1, state2, state3, state4, state5, state6, state7})

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
i = set([state0])

# Define the set of propositions
Prop = set(["c1", "c2"])

# Define the labeling function
l = {
    state0: ["nc1", "c2", "y=1"],
    state1: ["p1", "nc2", "y=1"],
    state2: ["nc1", "p2", "y=1"],
    state3: ["p1", "p2", "y=1"],
    state4: ["c1", "nc2", "y=0"],
    state5: ["nc1", "c2", "y=0"],
    state6: ["c1", "p2", "y=0"],
    state7: ["p1", "c2", "y=0"],
}

# Define the transition system
ST = TransitionSystem(s, Act, transitions, i, Prop, l)

# Define the invariant
Phi = Or(Not(Variable("c1")), Not(Variable("c2")))

# Verify the invariant
verify = verify()
result = verify.verify_invariant(ST, Phi)
if result[0] == "NON":
    print(result[0])
    print("Counterexample:")
    for state in result[1]:
        print(state.name)
else:
    print(result)
