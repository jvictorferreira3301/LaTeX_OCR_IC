import re

def extract_equations(input_file, output_file):
    # Regular expression for LaTeX equations in \begin{equation} ... \end{equation}, ignoring \label{}
    equation_pattern = r'\\begin\{equation\}(.+?)\\end\{equation\}'
    label_pattern = r'\\label\{[^}]*\}'  # Pattern to match and remove labels

    # Read input file and extract equations
    with open(input_file, 'r') as file:
        content = file.read()

        # Find all matches for the equation pattern
        equations = re.findall(equation_pattern, content, re.DOTALL)
        
        # Process each equation to remove labels and convert to a single line
        cleaned_equations = []
        for eq in equations:
            cleaned_eq = re.sub(label_pattern, '', eq)  # Remove label

            eq_lines = cleaned_eq.split('\n')

            poped = 0
            for i in range(len(eq_lines)):                
                if eq_lines[i - poped].replace(' ', '').startswith('%'):
                    eq_lines.pop(i - poped)
                    poped += 1

                if (len(eq_lines[i - poped].split('%')) > 1):
                    eq_lines[i - poped] = eq_lines[i - poped].split('%')[0]

            cleaned_eq = ''.join(eq_lines)

            cleaned_eq = re.sub(r'\s+', ' ', cleaned_eq)  # Replace multiple spaces/newlines with a single space
            cleaned_eq = cleaned_eq.strip()  # Trim leading and trailing spaces
            cleaned_equations.append(cleaned_eq)

    # Write each cleaned equation to a new line in the output file
    with open(output_file, 'w') as file:
        total_equations = 0
        for equation in cleaned_equations:
            if len(equation) > 0:
                file.write(equation + '\n')
                total_equations += 1

        print(f'Extracted {total_equations} usable equations!')

# Usage
input_tex_file = 'outputs/extracted_equations.tex'
output_txt_file = 'outputs/extracted_equations.txt'
extract_equations(input_tex_file, output_txt_file)
