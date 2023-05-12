from LR import canonical_collection
from LL import first_sets,follow_sets
from automata import visualize_lr0
import re


def read_yalp_file(filename):
    with open(filename, 'r') as file:
        content = file.read()
    return content

def split_sections(content):
    errorStack = []
    tokens_section = None
    productions_section = None
    sections = content.split('%%')
    if len(sections)!= 2:
        errorStack.append("Error: No se encuentra la división '%%' entre las secciones de tokens y producciones.")
    else:
        tokens_section = sections[0]
        productions_section = sections[1]
    return tokens_section, productions_section,errorStack

def process_tokens_section(content):
    tokens = []
    lines = content.split('\n')
    for line in lines:
        if line.startswith("%token"):
            line_tokens = line[len("%token"):].strip().split(' ')
            tokens.extend(line_tokens)
    return tokens


def process_productions_section(content):
    productions = {}
    lines = content.split('\n')
    current_production = None
    production_rules = []

    for line in lines:
        line = line.strip()
        if not line:
            continue

        if line.endswith(':'):
            if current_production:
                productions[current_production] = production_rules
                production_rules = []

            current_production = line[:-1]

        elif line.endswith(';'):
            line = line[:-1]
            if line:
                production_rules.append(line.strip())

            productions[current_production] = production_rules
            production_rules = []
            current_production = None

        else:
            if current_production:
                if '|' in line:
                    line = line.strip().split('|')
                    production_rules.extend(item.strip() for item in line if item.strip())
                else:
                    production_rules.append(line)

    return productions


def validate_yalp(tokens_section, productions_section, tokens, productions):
    error_stack = []

    # Check if '%%' division exists
    if not tokens_section or not productions_section:
        error_stack.append("Error: The '%%' division between tokens and productions sections is missing.")

    # Check if '%' symbol is present before token declaration
    lines = tokens_section.split('\n')
    for line in lines:
        if not line.startswith("%token") and not line.startswith("IGNORE") and line.strip():
            error_stack.append(f"Error: The '%' symbol is missing before the token declaration in line '{line.strip()}'.")
            break

    # Check if a production has the same name as a token
    for token in tokens:
        if token in productions:
            error_stack.append(f"Error: The production '{token}' has the same name as a token.")
            break

    return error_stack

def parse_yalp_file(filename,error_stack):
    content = read_yalp_file(filename)
    content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)  # Eliminar comentarios
    tokens_section, productions_section,divisionError = split_sections(content)
    tokens = None
    productions = None
    if(divisionError):
        error_stack.extend(divisionError)
    else:
        tokens = process_tokens_section(tokens_section)
        productions = process_productions_section(productions_section)

        error_stack.extend(validate_yalp(tokens_section, productions_section, tokens, productions))

    return tokens, productions,error_stack

def convert_productions(productions_dict):
    converted_productions = {}
    for key, value in productions_dict.items():
        converted_productions[key] = [rule.split() for rule in value]
    return converted_productions

