class DFA:
    def __init__(self, states, alphabet, transitions, start_state, accepting_states):
        self.states = states  # set of states
        self.alphabet = alphabet  # set of symbols
        self.transitions = transitions  # dictionary from state-symbol pair to state
        self.start_state = start_state  # subset of states
        self.accepting_states = accepting_states  # subset of states

    def __str__(self):
        output_str = "States : " + sorted(list(self.states)).__str__() + "\nAlphabet: " + \
        sorted(list(self.alphabet)).__str__() + "\nStart State: " + \
        str(self.start_state) + "\nAccepting states: " + \
        sorted(list(self.accepting_states)).__str__() + "\nTransitions:"
        for ((a, b), v) in self.transitions.items():
            output_str += ("[" + str(a) + "] -" + str(b) + "-> [" + str(v) + "] \n \t \t \t")
        return output_str

    def accepts(self, string):
        return self.process(string) in self.accepting_states

    def process(self, string, state=None):
        if state is None:
            state = self.start_state
        for c in string:
            state = self.transitions[(state, c)]
        return state

    def minimize(self):
        marked = set()  # a pair of states are marked if they cannot be merged
        unreachable = self.find_unreachable()
        self.states -= unreachable  # remove unreachable states
        for state in unreachable:  # remove transitions involving unreachable states
            for c in self.alphabet:
                del self.transitions[(state, c)]
        pairs = self.pairs(self.states - self.find_unreachable())
        for (p, q) in pairs:  # mark all pairs where one is an accepting state and the other is not
            if (p in self.accepting_states) & (q not in self.accepting_states) \
               | (q in self.accepting_states) & (p not in self.accepting_states):  # xor
                marked.add((p, q))
        changed = True
        while changed:  # while a pair has been marked in the last cycle
            unmarked = pairs - marked
            changed = False
            for (p, q) in unmarked:
                for c in self.alphabet:
                    r = self.transitions[(p, c)]
                    s = self.transitions[(q, c)]
                    if ((r, s) in marked) | ((s, r) in marked):
                        marked.add((p, q))
                        changed = True
        unmarked = pairs - marked
        for (p, q) in unmarked:
            to_merge = {p, q}
            for (r, s) in unmarked-{(p, q)}:
                if (p == r) | (p == s) | (q == r) | (q == s):  # shared elements between pairs merge to one state
                    to_merge.update({r, s})
            self.merge(to_merge)

    def merge(self, states):
        new_state = ''.join(states)  # name the merged state the concatenation of the old state's names
        update_dict = {}
        remove_keys = set()
        for state in states:
            if state in self.accepting_states:  # if any one state is accepting all will be
                self.accepting_states.add(new_state)
                self.accepting_states.remove(state)
            if state in self.start_state:  # as should the start state
                self.start_state = new_state
            for ((p, b), q) in self.transitions.items():  # update transitions to re-route through new state
                if q == state:
                    if p in states:
                        update_dict[(new_state, b)] = new_state
                        remove_keys.add(p)
                    else:
                        update_dict[(p, b)] = new_state
                if p == state:
                    if q in states:
                        update_dict[(new_state, b)] = new_state
                        remove_keys.add((p, b))
                        remove_keys.add(q)
                    else:
                        update_dict[(new_state, b)] = q
                        remove_keys.add((p, b))
        self.states = self.states - states
        self.states.add(new_state)
        for key in remove_keys:
            if key in self.transitions:
                del self.transitions[key]
        self.transitions.update(update_dict)  # update to the new transitions

    def find_unreachable(self):
        marked = {self.start_state}
        changed = True
        while changed:  # while a state has been marked in the last cycle
            changed = False  # will change to True if any state is marked in cycle
            for ((p, b), q) in self.transitions.items():
                # mark all states reachable via transition(s) from marked state(s)
                if (p in marked) & (q in (self.states - marked)):
                    marked.add(q)
                    changed = True
        return self.states - marked

    @staticmethod
    def pairs(states):
        pairs = set()
        for x in states:
            for y in states:
                if (x != y) & ((x, y) not in pairs) & ((y, x) not in pairs):
                    pairs.add((x, y))
        return pairs


# trans1 = {('q0', 'a'): 'q1', ('q0', 'b'): 'q3', ('q1', 'a'): 'q2', ('q1', 'b'): 'q3',
#          ('q2', 'a'): 'q0', ('q2', 'b'): 'q3', ('q3', 'a'): 'q1', ('q3', 'b'): 'q3'}
# machine1 = DFA({'q0', 'q1', 'q2', 'q3'}, {'a', 'b'}, trans1, 'q0', {'q3'})
# print(machine1)
# machine1.minimize()
# print(machine1)
#
# # same as trans1 but with a set of unreachable states
# trans2 = {('q0', 'a'): 'q1', ('q0', 'b'): 'q3', ('q1', 'a'): 'q2', ('q1', 'b'): 'q3',
#           ('q2', 'a'): 'q0', ('q2', 'b'): 'q3', ('q3', 'a'): 'q1', ('q3', 'b'): 'q3',
#           ('q4', 'a'): 'q5', ('q4', 'b'): 'q4', ('q5', 'a'): 'q4', ('q5', 'b'): 'q5'}
# machine2 = DFA({'q0', 'q1', 'q2', 'q3', 'q4', 'q5'}, {'a', 'b'}, trans2, 'q0', {'q3', 'q4', 'q5'})
# print(machine2)
# machine2.minimize()
# print(machine2)

trans3 = {('q0', 'a'): 'q1', ('q0', 'b'): 'q2', ('q1', 'a'): 'q2', ('q1', 'b'): 'q3', ('q2', 'a'): 'q4',
          ('q2', 'b'): 'q6', ('q3', 'a'): 'q4', ('q3', 'b'): 'q5', ('q4', 'a'): 'q3', ('q4', 'b'): 'q6',
          ('q5', 'a'): 'q5', ('q5', 'b'): 'q6', ('q6', 'a'): 'q5', ('q6', 'b'): 'q6'}
machine3 = DFA({'q0', 'q1', 'q2', 'q3', 'q4', 'q5', 'q6'}, {'a','b'}, trans3, 'q0', {'q5', 'q6'})
print(machine3)
machine3.minimize()
print(machine3)





