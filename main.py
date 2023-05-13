from yapar import *
from yalex import *

def read_yalex_content(filename):
    with open(filename, 'r') as f:
        return f.read()

def extract_regex_patterns():
    simple_pattern = r"\[(\w)\s*-\s*(\w)\]"
    compound_pattern = r"\[(\w)\s*-\s*(\w)\s*(\w)\s*-\s*(\w)\]"
    simple_regex_pattern = r"^let\s+\w+\s+=\s+(.*?)$"
    return simple_pattern, compound_pattern, simple_regex_pattern

def process_file_content(content):
    header_result, trailer_result, file_content, i = build_header_and_trailer(content)
    file_content = clean_comments(file_content)
    file_content = replace_quotation_mark(file_content)
    regex, errorStack, fin = build_regex(file_content, i)
    LEXtokens, errorStack = build_tokens(file_content, regex, errorStack, fin+1)
    return header_result, trailer_result, file_content, regex, LEXtokens, errorStack

def check_token_definitions(tokens, LEXtokens):
    gooTokens = []
    errorStack = []
    for token in tokens:
        for lex_token in LEXtokens:
            evald = evalToken(lex_token)
            if token == evald:
                gooTokens.append(token)
        if token not in gooTokens:
            errorStack.append(f"No se definió el token {token} en el yalex\n")
    if len(gooTokens) < len(LEXtokens):
        errorStack.append("No se definieron todos los tokens en el yalp\n")
    return gooTokens, errorStack

def convert_productions(productions):
    converted_productions = {}
    for key, value in productions.items():
        converted_productions[key] = [prod.split() for prod in value]
    return converted_productions

def visualize_lr0_states(states, transitions):
    
    print('Transiciones:')
    for transition in transitions:
        print(f'\t{transition}')
    visualize_lr0(states, transitions)

def print_first_and_follow_sets(productions_dict):
    converted_productions = convert_productions(productions_dict)
    first = first_sets(converted_productions)
    follow = follow_sets(converted_productions, first)
    print("First sets:")
    for non_terminal, first_set in first.items():
        print(f"{non_terminal}: {first_set}")
    print("\nFollow sets:")
    for non_terminal, follow_set in follow.items():
        print(f"{non_terminal}: {follow_set}")

# Main program
lex_filename = 'lex2.yal'
lexp_filename = 'lex2.yalp'

yalex_content = read_yalex_content(lex_filename)
simple_pattern, compound_pattern, simple_regex_pattern = extract_regex_patterns()
header_result, trailer_result, file_content, regex, LEXtokens, errorStack = process_file_content(yalex_content)

if errorStack:
    print("Error in the stack\n")
    for error in errorStack:
        print(error)
    exit()

tokens, productions_dict, errorStack = parse_yalp_file(lexp_filename, errorStack)
if errorStack:
    print("Error in the stack\n")
    for error in errorStack:
        print(error)
    exit()

gooTokens, tokenErrorStack = check_token_definitions(tokens, LEXtokens)

if tokenErrorStack:
    print("Error in the stack\n")
    for error in tokenErrorStack:
        print(error)
    exit()

if len(gooTokens) < len(LEXtokens):
    errorStack.append("Not all tokens were defined in yalp\n")

if errorStack:
    print("Error in the stack\n")
    for error in errorStack:
        print(error)
    exit()

converted_productions = convert_productions(productions_dict)

print(converted_productions, '\n')

states, transitions = canonical_collection(converted_productions)

visualize_lr0_states(states, transitions)

print("\nLL for first and follow functions\n")

print(productions_dict)
print_first_and_follow_sets(productions_dict)

