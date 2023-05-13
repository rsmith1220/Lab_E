from yapar import *
from yalex import *

with open('lex2.yal', 'r') as f:
    # Leer todas las líneas del archivo
    yalex_content = f.read()


header_result = ''
regex = {}
simple_pattern = r"\[(\w)\s*-\s*(\w)\]"
compound_pattern = r"\[(\w)\s*-\s*(\w)\s*(\w)\s*-\s*(\w)\]"
simple_regex_pattern = r"^let\s+\w+\s+=\s+(.*?)$"

# Llamando a las funciones en orden
file_content = yalex_content

header_result, trailer_result, file_content,i = build_header_and_trailer(file_content)
file_content = clean_comments(file_content)
file_content = replace_quotation_mark(file_content)
regex,errorStack,fin = build_regex(file_content,i)
LEXtokens,errorStack = build_tokens(file_content, regex,errorStack,fin+1)

tokens, productions_dict,errorStack = parse_yalp_file('lex2.yalp',errorStack)
if errorStack:
    print("error en el stack\n")
    for error in errorStack:
        print(error)
    exit()

gooTokens = []

for token in tokens:
    for lex_token in LEXtokens:
        evald = evalToken(lex_token)
        if token == evald:
            gooTokens.append(token)
    if token not in gooTokens:
        errorStack.append(f"No se definio el token {token} en el yalex\n")

if len(gooTokens) < len(LEXtokens):
    errorStack.append("No se definieron todos los tokens en el yalp\n")


if errorStack:
    print("error en el stack\n")
    for error in errorStack:
        print(error)
    exit()

converted_productions = convert_productions(productions_dict)
print(converted_productions,'\n')


states, transitions = canonical_collection(converted_productions)

print('Estados:')
for i, state in enumerate(states):
    print('\t',f'{i}: {state}')

print('Transiciones:')
for transition in transitions:
    print('\t',transition)
# Ejemplo de uso:

visualize_lr0(states, transitions)

print("\nLL para funciones primero y siguiente\n")

def convert_productions(productions):
    converted_productions = {}
    for key, value in productions.items():
        converted_productions[key] = [prod.split() for prod in value]
    return converted_productions

print(productions_dict)
converted_prod = convert_productions(productions_dict)
first = first_sets(converted_prod)
follow = follow_sets(converted_prod, first)

print("First sets:")
for non_terminal, first_set in first.items():
    print(f"{non_terminal}: {first_set}")

print("\nFollow sets:")
for non_terminal, follow_set in follow.items():
    print(f"{non_terminal}: {follow_set}")
