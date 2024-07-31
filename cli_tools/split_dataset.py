import os
import argparse
import shutil
import random

def parse_args():
    parser = argparse.ArgumentParser(description='Split dataset into train, validation, and test sets.')
    parser.add_argument('--input_dir', required=True, help='Directory containing the dataset')
    parser.add_argument('--train_ratio', type=float, required=True, help='Ratio of the dataset to use for training')
    parser.add_argument('--val_ratio', type=float, required=True, help='Ratio of the dataset to use for validation')
    parser.add_argument('--test_ratio', type=float, required=True, help='Ratio of the dataset to use for testing')
    parser.add_argument('--output_dir', required=True, help='Directory to save the split datasets')
    return parser.parse_args()

def split_dataset(input_dir, train_ratio, val_ratio, test_ratio, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Paths for train, val, and test directories
    train_dir = os.path.join(output_dir, 'train')
    val_dir = os.path.join(output_dir, 'val')
    test_dir = os.path.join(output_dir, 'test')

    for directory in [train_dir, val_dir, test_dir]:
        if not os.path.exists(directory):
            os.makedirs(directory)

    # Collect all files
    all_files = [f for f in os.listdir(input_dir) if f.endswith(('.jpg', '.png', '.jpeg'))]

    # Shuffle files
    random.shuffle(all_files)
    
    # Calculate split indices
    total_files = len(all_files)
    train_end = int(train_ratio * total_files)
    val_end = train_end + int(val_ratio * total_files)

    # Split data
    train_files = all_files[:train_end]
    val_files = all_files[train_end:val_end]
    test_files = all_files[val_end:]

    # Function to copy files to respective directories
    def copy_files(file_list, target_dir):
        for file in file_list:
            shutil.copy(os.path.join(input_dir, file), os.path.join(target_dir, file))

    copy_files(train_files, train_dir)
    copy_files(val_files, val_dir)
    copy_files(test_files, test_dir)

    print(f"Dataset split completed. Training set: {len(train_files)} files, Validation set: {len(val_files)} files, Test set: {len(test_files)} files")

if __name__ == '__main__':
    args = parse_args()
    split_dataset(args.input_dir, args.train_ratio, args.val_ratio, args.test_ratio, args.output_dir)

