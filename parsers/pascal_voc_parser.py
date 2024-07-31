import xml.etree.ElementTree as ET

class PascalVOCParser:
    def __init__(self, file_path=None):
        self.file_path = file_path

    def parse(self):
        tree = ET.parse(self.file_path)
        root = tree.getroot()
        annotations = {
            'folder': root.find('folder').text if root.find('folder') is not None else None,
            'filename': root.find('filename').text if root.find('filename') is not None else None,
            'path': root.find('path').text if root.find('path') is not None else None,
            'size': {
                'width': int(root.find('size/width').text) if root.find('size/width') is not None else None,
                'height': int(root.find('size/height').text) if root.find('size/height') is not None else None,
                'depth': int(root.find('size/depth').text) if root.find('size/depth') is not None else None,
            },
            'objects': []
        }
        for obj in root.findall('object'):
            annotations['objects'].append({
                'name': obj.find('name').text if obj.find('name') is not None else None,
                'pose': obj.find('pose').text if obj.find('pose') is not None else None,
                'truncated': int(obj.find('truncated').text) if obj.find('truncated') is not None else None,
                'difficult': int(obj.find('difficult').text) if obj.find('difficult') is not None else None,
                'bndbox': {
                    'xmin': int(obj.find('bndbox/xmin').text) if obj.find('bndbox/xmin') is not None else None,
                    'ymin': int(obj.find('bndbox/ymin').text) if obj.find('bndbox/ymin') is not None else None,
                    'xmax': int(obj.find('bndbox/xmax').text) if obj.find('bndbox/xmax') is not None else None,
                    'ymax': int(obj.find('bndbox/ymax').text) if obj.find('bndbox/ymax') is not None else None,
                }
            })
        return annotations

    def to_xml(self, data, output_file):
        root = ET.Element("annotation")
        ET.SubElement(root, "folder").text = data['folder']
        ET.SubElement(root, "filename").text = data['filename']
        ET.SubElement(root, "path").text = data['path']
        source = ET.SubElement(root, "source")
        ET.SubElement(source, "database").text = "Unknown"
        size = ET.SubElement(root, "size")
        ET.SubElement(size, "width").text = str(data['size']['width'])
        ET.SubElement(size, "height").text = str(data['size']['height'])
        ET.SubElement(size, "depth").text = str(data['size']['depth'])
        ET.SubElement(root, "segmented").text = "0"
        for obj in data['objects']:
            obj_elem = ET.SubElement(root, "object")
            ET.SubElement(obj_elem, "name").text = obj['name']
            ET.SubElement(obj_elem, "pose").text = obj['pose']
            ET.SubElement(obj_elem, "truncated").text = str(obj['truncated'])
            ET.SubElement(obj_elem, "difficult").text = str(obj['difficult'])
            bndbox = ET.SubElement(obj_elem, "bndbox")
            ET.SubElement(bndbox, "xmin").text = str(obj['bndbox']['xmin'])
            ET.SubElement(bndbox, "ymin").text = str(obj['bndbox']['ymin'])
            ET.SubElement(bndbox, "xmax").text = str(obj['bndbox']['xmax'])
            ET.SubElement(bndbox, "ymax").text = str(obj['bndbox']['ymax'])
        tree = ET.ElementTree(root)
        tree.write(output_file)