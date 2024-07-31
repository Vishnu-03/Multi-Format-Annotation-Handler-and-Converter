import json

class COCOParser:
    def __init__(self, file_path=None):
        self.file_path = file_path

    def parse(self):
        with open(self.file_path, 'r') as f:
            data = json.load(f)
        return data

    def to_json(self, data, output_file):
        with open(output_file, 'w') as f:
            json.dump(data, f, indent=4)
