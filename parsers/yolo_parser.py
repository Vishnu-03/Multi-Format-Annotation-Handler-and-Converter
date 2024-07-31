class YOLOParser:
    def __init__(self, file_path):
        self.file_path = file_path

    def parse(self):
        annotations = []
        with open(self.file_path, 'r') as file:
            for line in file:
                parts = line.strip().split()
                if len(parts) == 5:
                    try:
                        # Convert values to float
                        class_id = int(parts[0])  # Ensure class_id is an integer
                        x_center = float(parts[1])
                        y_center = float(parts[2])
                        width = float(parts[3])
                        height = float(parts[4])
                        annotations.append([class_id, x_center, y_center, width, height])
                    except ValueError:
                        print(f"Skipping invalid line: {line.strip()}")
        return annotations




    def to_txt(self, data, output_file):
        with open(output_file, 'w') as f:
            for ann in data:
                line = f"{ann['class_id']} {ann['center_x']} {ann['center_y']} {ann['width']} {ann['height']}\n"
                f.write(line)
