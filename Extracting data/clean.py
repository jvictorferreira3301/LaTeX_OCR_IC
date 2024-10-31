import os
from pathlib import Path

def remove_tex_files(directory):
    """Remove all .tex, .pdf, .aux, and .log files from the specified directory."""
    # Convert the directory to a Path object
    dir_path = Path(directory)

    # Check if the directory exists
    if not dir_path.is_dir():
        print(f"The directory {directory} does not exist.")
        return

    # Iterate over all files in the directory
    for file in dir_path.glob('*'):
        # Check for specific file extensions and remove them
        if file.suffix in ['.tex', '.pdf', '.aux', '.log']:
            try:
                file.unlink()  # Remove the file
                print(f"Removed: {file}")
            except Exception as e:
                print(f"Error removing {file}: {e}")

# Usage
directory = './'  # Replace with your directory path
remove_tex_files(directory)
