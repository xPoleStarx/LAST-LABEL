import cv2
import json
import matplotlib.pyplot as plt

def parse_json(json_file):
    with open(json_file, 'r') as file:
        data = json.load(file)
    boxes = []
    for obj in data['objects']:
        bbox = obj['bndbox']
        xmin = int(bbox['xmin'])
        ymin = int(bbox['ymin'])
        xmax = int(bbox['xmax'])
        ymax = int(bbox['ymax'])
        boxes.append((xmin, ymin, xmax, ymax))
    return boxes

def draw_bounding_boxes(image_path, boxes):
    image = cv2.imread(image_path)
    for box in boxes:
        cv2.rectangle(image, (box[0], box[1]), (box[2], box[3]), (0, 255, 0), 2)
    return image

def show_image(image):
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.axis('off')
    plt.show()

json_file = 'sensor_1.json'
image_path = 'sensor_1.png'

boxes = parse_json(json_file)
image_with_boxes = draw_bounding_boxes(image_path, boxes)
show_image(image_with_boxes)
