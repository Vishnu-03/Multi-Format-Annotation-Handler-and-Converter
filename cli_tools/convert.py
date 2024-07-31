import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from parsers.pascal_voc_parser import PascalVOCParser
from parsers.coco_parser import COCOParser
from parsers.labelme_parser import LabelMeParser
from parsers.yolo_parser import YOLOParser
import argparse

def parse_annotations(input_dir, source_format):
    annotations = []
    if source_format == 'voc':
        parser = PascalVOCParser()
        for file_name in os.listdir(input_dir):
            if file_name.endswith('.xml'):
                parser.file_path = os.path.join(input_dir, file_name)
                annotations.append(parser.parse())
    elif source_format == 'coco':
        parser = COCOParser(os.path.join(input_dir, 'annotations.json'))
        annotations = parser.parse()
    elif source_format == 'labelme':
        parser = LabelMeParser()
        for file_name in os.listdir(input_dir):
            if file_name.endswith('.json'):
                parser.file_path = os.path.join(input_dir, file_name)
                annotations.append(parser.parse())
    elif source_format == 'yolo':
        parser = YOLOParser()
        for file_name in os.listdir(input_dir):
            if file_name.endswith('.txt'):
                parser.file_path = os.path.join(input_dir, file_name)
                annotations.append(parser.parse())
    return annotations

def write_annotations(annotations, output_dir, target_format):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    if target_format == 'voc':
        parser = PascalVOCParser()
        for i, annotation in enumerate(annotations):
            output_file = os.path.join(output_dir, f'{i:06d}.xml')
            parser.to_xml(annotation, output_file)
    elif target_format == 'coco':
        parser = COCOParser()
        output_file = os.path.join(output_dir, 'annotations.json')
        parser.to_json(annotations, output_file)
    elif target_format == 'labelme':
        parser = LabelMeParser()
        for i, annotation in enumerate(annotations):
            output_file = os.path.join(output_dir, f'{i:06d}.json')
            parser.to_json(annotation, output_file)
    elif target_format == 'yolo':
        parser = YOLOParser()
        for i, annotation in enumerate(annotations):
            output_file = os.path.join(output_dir, f'{i:06d}.txt')
            parser.to_txt(annotation, output_file)

def convert(input_dir, output_dir, source_format, target_format):
    annotations = parse_annotations(input_dir, source_format)
    write_annotations(annotations, output_dir, target_format)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert annotation formats.')
    parser.add_argument('--input_dir', type=str, required=True, help='Path to the input directory.')
    parser.add_argument('--output_dir', type=str, required=True, help='Path to the output directory.')
    parser.add_argument('--source_format', type=str, required=True, choices=['voc', 'coco', 'labelme', 'yolo'], help='Source annotation format.')
    parser.add_argument('--target_format', type=str, required=True, choices=['voc', 'coco', 'labelme', 'yolo'], help='Target annotation format.')
    args = parser.parse_args()
    
    convert(args.input_dir, args.output_dir, args.source_format, args.target_format)
