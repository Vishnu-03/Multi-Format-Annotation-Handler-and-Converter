import csv
import json
import os
import argparse
from parsers.pascal_voc_parser import PascalVOCParser
from parsers.coco_parser import COCOParser
from parsers.labelme_parser import LabelMeParser
from parsers.yolo_parser import YOLOParser

def parse_annotations(input_dir, source_format):
    annotations = []
    if source_format == 'voc':
        parser = PascalVOCParser()
        for file_name in os.listdir(input_dir):
            if file_name.endswith('.xml'):
                parser.file_path = os.path.join(input_dir, file_name)
                annotations.extend(parser.parse())  # Ensure it's a list of annotations
    elif source_format == 'coco':
        for file_name in os.listdir(input_dir):
            if file_name.endswith('.json'):
                parser = COCOParser(os.path.join(input_dir, file_name))
                annotations = parser.parse()
                if isinstance(annotations, dict) and 'shapes' in annotations:
                    annotations = annotations['shapes']
                break  # Assuming there's only one COCO JSON file
    elif source_format == 'labelme':
        parser = LabelMeParser()
        for file_name in os.listdir(input_dir):
            if file_name.endswith('.json'):
                parser.file_path = os.path.join(input_dir, file_name)
                annotations.extend(parser.parse())  # Ensure it's a list of annotations
    elif source_format == 'yolo':
        parser = YOLOParser()
        for file_name in os.listdir(input_dir):
            if file_name.endswith('.txt'):
                parser.file_path = os.path.join(input_dir, file_name)
                annotations.extend(parser.parse())  # Ensure it's a list of annotations
    print(f"Parsed annotations: {annotations}")  # Debug print
    return annotations

def annotations_to_csv(annotations, output_file):
    if annotations:
        print(f"Type of annotations: {type(annotations)}")
        if isinstance(annotations, list) and isinstance(annotations[0], dict):
            keys = annotations[0].keys()
            with open(output_file, mode='w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=keys)
                writer.writeheader()
                for annotation in annotations:
                    writer.writerow(annotation)
        else:
            print("Unexpected format for annotations.")
            if isinstance(annotations, dict):
                # Handle case where annotations is a dictionary
                print("Annotations dictionary:", annotations)
                # Implement logic to convert dictionary to CSV if needed
    else:
        print("No annotations to write to CSV.")

def main():
    parser = argparse.ArgumentParser(description="Export annotations to CSV.")
    parser.add_argument('--input_dir', type=str, required=True, help="Directory containing annotation files.")
    parser.add_argument('--format', type=str, choices=['voc', 'coco', 'labelme', 'yolo'], required=True, help="Annotation format.")
    parser.add_argument('--output_file', type=str, required=True, help="Path to output CSV file.")
    args = parser.parse_args()

    annotations = parse_annotations(args.input_dir, args.format)
    annotations_to_csv(annotations, args.output_file)

if __name__ == "__main__":
    main()
