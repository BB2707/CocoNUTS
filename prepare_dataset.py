import os
import shutil
import random

def split_dataset(base_dir, output_dir, split_ratio=0.8):
    """
    Splits a dataset of images into training and validation sets.

    Args:
        base_dir (str): Path to the original dataset with class subfolders.
        output_dir (str): Path to the directory where the split dataset will be saved.
        split_ratio (float): The proportion of images to be used for training.
    """
    print(f"Preparing to split dataset from '{base_dir}' into '{output_dir}'...")

    # Create the output directories if they don't exist
    train_dir = os.path.join(output_dir, 'train')
    validation_dir = os.path.join(output_dir, 'validation')

    if os.path.exists(output_dir):
        print(f"Output directory '{output_dir}' already exists. Deleting it to start fresh.")
        shutil.rmtree(output_dir)

    os.makedirs(train_dir, exist_ok=True)
    os.makedirs(validation_dir, exist_ok=True)

    # Get the class names from the subfolder names in the base directory
    class_names = [d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))]

    if not class_names:
        print(f"Error: No class subfolders found in '{base_dir}'. Please check the path.")
        return

    print(f"Found {len(class_names)} classes: {class_names}")

    # Process each class
    for class_name in class_names:
        print(f"\nProcessing class: {class_name}")
        
        # Create subdirectories in train and validation folders
        os.makedirs(os.path.join(train_dir, class_name), exist_ok=True)
        os.makedirs(os.path.join(validation_dir, class_name), exist_ok=True)
        
        # Get all image file names for the current class
        source_dir = os.path.join(base_dir, class_name)
        all_files = [f for f in os.listdir(source_dir) if os.path.isfile(os.path.join(source_dir, f))]
        
        # Shuffle the files to ensure a random split
        random.shuffle(all_files)
        
        # Determine the split index
        split_index = int(len(all_files) * split_ratio)
        
        # Get the training and validation file lists
        train_files = all_files[:split_index]
        validation_files = all_files[split_index:]
        
        print(f"  - Total images: {len(all_files)}")
        print(f"  - Assigning {len(train_files)} to training set.")
        print(f"  - Assigning {len(validation_files)} to validation set.")

        # Copy files to the training directory
        for file_name in train_files:
            shutil.copy(os.path.join(source_dir, file_name), os.path.join(train_dir, class_name, file_name))
            
        # Copy files to the validation directory
        for file_name in validation_files:
            shutil.copy(os.path.join(source_dir, file_name), os.path.join(validation_dir, class_name, file_name))

    print("\nDataset splitting completed successfully!")


if __name__ == '__main__':
    # --- Configuration ---
    # The path to your original, unsplit dataset
    original_dataset_dir = 'Coconut_Tree_Disease_Dataset' 
    # The name for the new, properly structured dataset folder
    split_dataset_dir = 'Coconut_Dataset_Split'

    # Check if the original dataset exists before running
    if not os.path.exists(original_dataset_dir):
        print(f"FATAL ERROR: The source dataset folder '{original_dataset_dir}' was not found.")
        print("Please make sure your dataset is in the correct location before running this script.")
    else:
        split_dataset(original_dataset_dir, split_dataset_dir)
