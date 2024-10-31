# 70% ChatGPT :D

import os
import re
from pathlib import Path

def load_macros(macros_file):
    """Reads macros from a LaTeX macros file and returns a dictionary of replacements."""
    macros = {}
    macro_pattern = r'\\(?:def|newcommand)\s*\\(\w+)\s*(?:\[(.*?)\])?\s*(\{(.*)\})'
    
    with open(macros_file, 'r') as file:
        for line in file:
            match = re.match(macro_pattern, line.strip())
            if match:
                command, _, definition, inside_def = match.groups()

                macros[rf'\\{command}'] = inside_def  # Store macro with regex-escaped backslash

                # print(f'{command} {inside_def}')
            
    return macros

def replacement_function(match, definition, param_mapping):
    if len(param_mapping) > 0:
        print(f'{match} {definition} {param_mapping}')

def replace_macros(equations, macros):
    """Replaces macros in equations using the given macros dictionary, ensuring standalone replacements."""
    for i, equation in enumerate(equations):
        for macro, definition in macros.items():
            # Replace each macro with its definition
            # This regex captures the argument inside the curly braces
            equation = re.sub(
                rf'(?<!\\)({macro})\{{(.*?)\}}',  # Match macro and its argument
                lambda match: definition.replace('#1', match.group(2).replace('$', '')),  # Replace #1 with the captured argument
                equation
            )
          

        equations[i] = equation
    return equations

def replace_macros2(equations, macros):
    """Replaces macros in equations using the given macros dictionary, ensuring standalone replacements."""
    for i, equation in enumerate(equations):
        for macro, definition in macros.items():
            # Check if the definition contains placeholders
            param_pattern = re.findall(r'#(\d+)', definition)

            # Create a mapping for parameters if there are placeholders
            param_mapping = {}
            for j in range(len(param_pattern)):
                param_index = int(param_pattern[j]) - 1  # Convert to 0-based index
                # Capture parameters from the equation based on their positions
                matches = re.findall(r'(\{.*?\}|\S+)', equation)  # Capture everything in braces and standalone words
                if param_index < len(matches):
                    param_mapping[f'#{j + 1}'] = matches[param_index]

            # Replace each macro using a lambda to avoid escape sequence issues
            equation = re.sub(
                rf'(?<!\\)({macro})(?![a-zA-Z0-9])',
                lambda match: re.sub(
                    r'(#\d+)',
                    lambda m: param_mapping.get(m.group(0), m.group(0)),  # Substitute placeholders with mapped values
                    definition
                ),
                equation
            )
        equations[i] = equation
    return equations

def extract_equations(input_tex_file, macros_file):
    # Load macros from macros_file
    macros = load_macros(macros_file)
    
    # Regular expressions to match equations
    equation_patterns = [
        # r'\$\$(.*?)\$\$',            # Inline equations with $$ ... $$
        # r'\$(.*?)\$',                # Inline equations with $ ... $
        r'\\\[(.*?)\\\]',            # Displayed equations with \[ ... \]
        r'\\begin\{equation\}(.*?)\\end\{equation\}',  # equation environment
        # r'\\begin\{align\}(.*?)\\end\{align\}'         # align environment
    ]
    
    # Read the input LaTeX file
    with open(input_tex_file, 'r') as file:
        tex_content = file.read()
    
    # Find all matches for each pattern
    equations = []
    for pattern in equation_patterns:
        matches = re.findall(pattern, tex_content, re.DOTALL)
        equations.extend(matches)
    
    # Replace macros in equations
    equations = replace_macros(equations, macros)
    equations = replace_macros2(equations, macros)

    return equations
    
tex_files_folder = 'bootor_tex'

output_tex_file = f'outputs/extracted_equations.tex'

macros_file = 'macros/macros.tex'

total_equations = 0

if not os.path.exists('outputs'):
        os.mkdir('outputs')

# Write equations to a new .tex file
with open(output_tex_file, 'w') as output_file:
    output_file.write('\\documentclass{article}\n')
    output_file.write('\\usepackage{amsmath}\n')
    output_file.write('\\usepackage{amssymb}\n')
    output_file.write('\\begin{document}\n')

    for subfolder in Path(tex_files_folder).glob('*'):

        for file in subfolder.glob('*'):
            equations = extract_equations(file, macros_file)

            # Write each extracted equation
            for eq in equations:
                output_file.write('\n\\begin{equation}\n')
                output_file.write(eq.strip())
                output_file.write('\n\\end{equation}\n')

            print(f"Extracted {len(equations)} equations from {file}.")
            total_equations = total_equations + len(equations)

    # Write end of the document
    output_file.write('\\end{document}\n')

print(f'Found {total_equations} equations in the folder {tex_files_folder}')