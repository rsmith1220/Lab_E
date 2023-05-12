def get_terminals_and_non_terminals(productions):
    non_terminals = set(productions.keys())
    terminals = set()

    for non_terminal in non_terminals:
        for production in productions[non_terminal]:
            for symbol in production:
                if symbol not in non_terminals:
                    terminals.add(symbol)

    return terminals, non_terminals

def first_sets(productions):
    terminals, non_terminals = get_terminals_and_non_terminals(productions)
    first = {non_terminal: set() for non_terminal in non_terminals}

    changed = True
    while changed:
        changed = False
        for non_terminal in non_terminals:
            for production in productions[non_terminal]:
                for symbol in production:
                    if symbol in terminals:
                        # For each terminal in the production, add it to the 'first' set
                        if symbol not in first[non_terminal]:
                            first[non_terminal].add(symbol)
                            changed = True
                        break
                    else:
                        # If the symbol is a non-terminal, add its 'first' set to the current non-terminal's 'first' set
                        added = len(first[non_terminal])
                        first[non_terminal].update(first[symbol] - {None})
                        if len(first[non_terminal]) != added:
                            changed = True
                        if None not in first[symbol]:
                            break
                else:
                    # If all symbols in the production can generate the empty string (None), add None to the 'first' set
                    if None not in first[non_terminal]:
                        first[non_terminal].add(None)
                        changed = True

    return first

def follow_sets(productions, first_sets):
    _, non_terminals = get_terminals_and_non_terminals(productions)
    follow = {non_terminal: set() for non_terminal in non_terminals}
    start_symbol = next(iter(non_terminals))
    follow[start_symbol].add('$')

    changed = True
    while changed:
        changed = False
        for non_terminal in non_terminals:
            for production in productions[non_terminal]:
                for i, symbol in enumerate(production):
                    if symbol in non_terminals:
                        if i + 1 < len(production):
                            next_symbol = production[i + 1]
                            if next_symbol in non_terminals:
                                added = len(follow[symbol])
                                follow[symbol].update(first_sets[next_symbol] - {None})
                                if len(follow[symbol]) != added:
                                    changed = True
                            else:
                                if next_symbol not in follow[symbol]:
                                    follow[symbol].add(next_symbol)
                                    changed = True
                        else:
                            added = len(follow[symbol])
                            follow[symbol].update(follow[non_terminal])
                            if len(follow[symbol]) != added:
                                changed = True

    return follow
