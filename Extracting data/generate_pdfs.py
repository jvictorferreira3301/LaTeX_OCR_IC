import os
from pathlib import Path
import re
import subprocess
from concurrent.futures import ThreadPoolExecutor

def extract_equations(input_txt_file):
    """Extract equations from the input .txt file, each line being an equation."""
    equations = []
    with open(input_txt_file, 'r') as file:
        # Read each line and strip any extra whitespace
        for line in file:
            stripped_line = line.strip()
            if stripped_line:  # Only add non-empty lines
                equations.append(stripped_line)
    return equations

def create_tex_file(equation, index):
    """Create a .tex file for the given equation."""
    tex_content = r"""\documentclass{article}
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{xcolor}
\begin{document}
\pagestyle{empty}
\begin{equation*}
""" + equation + r"""
\end{equation*}
\end{document}
"""
    file_name = f"{str(index).zfill(5)}.tex"
    with open(file_name, 'w') as file:
        file.write(tex_content)
    return file_name

def compile_tex_file(tex_file):
    """Compile the .tex file using XeLaTeX."""
    subprocess.run(['xelatex', tex_file], check=True)

def compile_tex_files(tex_files):
    """Compile multiple .tex files concurrently."""
    with ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(compile_tex_file, tex_files)

def main(input_tex_file):
    if not os.path.exists('outputs/pdfs'):
        os.makedirs('outputs/pdfs')

    equations = extract_equations(input_tex_file)

    tex_files = []
    for index, equation in enumerate(equations):
        tex_file = create_tex_file(equation.strip(), index)
        tex_files.append(tex_file)

    # Compile all .tex files concurrently
    compile_tex_files(tex_files)

    # Move PDFs to the output directory and clean up auxiliary files
    for tex_file in tex_files:
        pdf_file = Path(tex_file).with_suffix('.pdf')
        if pdf_file.exists():
            pdf_file.rename(Path('outputs/pdfs') / pdf_file.name)
            # Clean up auxiliary files
            os.remove(tex_file)
            os.remove(tex_file.replace('.tex', '.aux'))
            os.remove(tex_file.replace('.tex', '.log'))

if __name__ == "__main__":
    input_tex_file = 'outputs/extracted_equations.txt'
    main(input_tex_file)