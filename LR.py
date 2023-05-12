class LR0Item:
    def __init__(self, production, position,derived=False):
        self.production = (production[0], tuple(production[1]))
        self.position = position
        self.derived = derived
        

    def __repr__(self):
        return f'{self.production[0]} -> {" ".join(self.production[1][:self.position]) + "•" + " ".join(self.production[1][self.position:])}'

    def __eq__(self, other):
        return self.production == other.production and self.position == other.position

    def __hash__(self):
        return hash((self.production, self.position))
    
def closure(items, productions):
    new_items = set(items)
    changed = True
    while changed:
        changed = False
        for item in list(new_items):
            if item.position < len(item.production[1]) and item.production[1][item.position] in productions:
                non_terminal = item.production[1][item.position]
                for production in productions[non_terminal]:
                    new_item = LR0Item((non_terminal, production), 0, True)
                    if new_item not in new_items:
                        new_items.add(new_item)
                        changed = True
    return new_items

def goto(items, symbol, productions):
    next_items = set()
    for item in items:
        if item.position < len(item.production[1]) and item.production[1][item.position] == symbol:
            next_items.add(LR0Item(item.production, item.position + 1))
    return closure(next_items, productions)


def canonical_collection(productions):
    start_symbol = list(productions.keys())[0] + "'"
    items = LR0Item((start_symbol, [list(productions.keys())[0]]), 0)
    states = [closure({items}, productions)]
    transitions = []
    queue = [0]

    while queue:
        state_idx = queue.pop(0)
        state = states[state_idx]

        for symbol in set(sym for item in state for sym in item.production[1][item.position:item.position + 1]):
            next_state = goto(state, symbol, productions)
            if not next_state:
                continue
            if next_state not in states:
                states.append(next_state)
                queue.append(len(states) - 1)
            next_state_idx = states.index(next_state)
            transitions.append((state_idx, symbol, next_state_idx))

    # Add accept state
    accept_state = len(states)
    for i, state in enumerate(states):
        for item in state:
            if item.production[0] == start_symbol and item.position == len(item.production[1]) and item.derived == False:
                transitions.append((i, '$', accept_state))
                break
    states.append(set())

    return states, transitions
