## About
This code was made to extract data to train a ViT model that takes an image of a math formula and returns corresponding LaTeX code.

## Usage
1. Extract all equations from .tex files to a single .tex using ```extract_equations.py```

2. Parse extracted equations to a .txt where each line will be a different equation using ```equations_to_txt.py```

3. Compile extracted equations to PDF (each equation generates a different file) using ```generate_pdfs.py```

4. Convert PDF files to PNG images using ```pdf_to_png.py```