import os
import shutil
import random

def separate_files(source_dir, train_dir, test_dir, val_dir, train_ratio=0.7, test_ratio=0.2):
    """Randomly separates files from source_dir into train_dir, test_dir, and val_dir."""
    # Ensure the output directories exist
    os.makedirs(train_dir, exist_ok=True)
    os.makedirs(test_dir, exist_ok=True)
    os.makedirs(val_dir, exist_ok=True)

    # Get a list of all files in the source directory
    files = [f for f in os.listdir(source_dir) if os.path.isfile(os.path.join(source_dir, f))]
    
    # Shuffle the files randomly
    random.shuffle(files)

    # Calculate the number of files for each split
    total_files = len(files)
    train_count = int(total_files * train_ratio)
    test_count = int(total_files * test_ratio)
    val_count = total_files - train_count - test_count  # Remaining files go to validation

    # Separate the files into train, test, and validation sets
    for i, file in enumerate(files):
        src_path = os.path.join(source_dir, file)
        if i < train_count:
            shutil.move(src_path, os.path.join(train_dir, file))
        elif i < train_count + test_count:
            shutil.move(src_path, os.path.join(test_dir, file))
        else:
            shutil.move(src_path, os.path.join(val_dir, file))

    print(f"Separated {total_files} files into:")
    print(f"- {train_count} training files")
    print(f"- {test_count} testing files")
    print(f"- {val_count} validation files")

# Usage
dataset_dir = '../Datasets/bootor/'
source_directory = dataset_dir + 'images'  # Replace with your source directory
train_directory = dataset_dir + 'train'           # Replace with your train directory
test_directory = dataset_dir + 'test'             # Replace with your test directory
val_directory = dataset_dir + 'val'        # Replace with your validation directory

separate_files(source_directory, train_directory, test_directory, val_directory)
