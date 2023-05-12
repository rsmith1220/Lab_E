from graphviz import Digraph


def visualize_lr0(states, transitions):
    dot = Digraph("LR0", format='png')
    dot.attr(rankdir="LR")
    dot.attr('node', shape='rectangle')

    for i, state in enumerate(states):
        if i == len(states) - 1:  # Accept state
            label = 'ACCEPT'
        else:
            non_derived = [str(item) for item in state if not item.derived]
            derived = [str(item) for item in state if item.derived]

            label = f'I{i}\n-----------\n'
            label += '\n'.join(non_derived) + '\n-----------\n' + '\n'.join(derived)

        dot.node(str(i), label=label)

    for t in transitions:
        dot.edge(str(t[0]), str(t[2]), label=str(t[1]))

    # Generate and save the graph as a PNG image
    dot.render("automataLR(0)", cleanup=True)
