def get_terminals_and_non_terminals(productions):
    non_terminals = set(productions.keys())
    terminals = set()

    for non_terminal in non_terminals:
        for production in productions[non_terminal]:
            for symbol in production:
                if symbol not in non_terminals:
                    terminals.add(symbol)

    return terminals, non_terminals