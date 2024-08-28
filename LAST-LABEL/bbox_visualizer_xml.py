import cv2
import matplotlib.pyplot as plt
from lxml import etree

def parse_xml(xml_file):
    tree = etree.parse(xml_file)
    root = tree.getroot()
    boxes = []
    for object_tag in root.findall('object'):
        bbox = object_tag.find('bndbox')
        xmin = int(bbox.find('xmin').text)
        ymin = int(bbox.find('ymin').text)
        xmax = int(bbox.find('xmax').text)
        ymax = int(bbox.find('ymax').text)
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

xml_file = 'sensor_1.xml'
image_path = 'sensor_1.png'

boxes = parse_xml(xml_file)
image_with_boxes = draw_bounding_boxes(image_path, boxes)
show_image(image_with_boxes)
