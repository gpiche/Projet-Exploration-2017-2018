import pandas as pd
import cv2
import numpy as np
from scipy import ndimage



class ImageManager:

    def __init__(self):
        self.bounding_info = [0, 0, 0, 0]

    def get_image_info(self, image_paths, output_path, index=False):
        value_list = []
        for image in image_paths:
            img = cv2.imread(image, 1)
            height, width = self.get_size(img)
            xmin, ymin, xmax, ymax = self.get_bounds(img)
            normalised_image = np.mean(img, dtype=np.double)
            value = (width, height, xmin, ymin, xmax, ymax, normalised_image)

            if index is True:
                for key in image_paths.values():
                    if image_paths[image] == key:
                        value += (key,)
                        break
            value_list.append(value)

        self.create_csv_file(output_path, index, value_list)

    @staticmethod
    def create_csv_file(output_path, index, value_list):
        if index is False:
            column_name = ['width', 'height', 'xmin', 'ymin', 'xmax', 'ymax', 'normalised_value']
        else:
            column_name = ['width', 'height', 'xmin', 'ymin', 'xmax', 'ymax', 'normalised_value', 'class_id']

        xml_df = pd.DataFrame(value_list, columns=column_name)
        xml_df.to_csv(output_path, index=None)

    @staticmethod
    def get_size(img):
        return img.shape[:2]

    @staticmethod
    def get_bounds(image):
        net = cv2.dnn.readNetFromCaffe('tracker/MobileNetSSD_deploy.prototxt.txt',
                                       'tracker/MobileNetSSD_deploy.caffemodel')
        (h, w) = image.shape[:2]
        blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 0.007843, (300, 300), 127.5)
        net.setInput(blob)
        detections = net.forward()
        start_x, start_y, end_x, end_y = 0, 0, 0, 0

        for i in np.arange(0, detections.shape[2]):
            confidence = detections[0, 0, i, 2]

            if confidence > 0.2:
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (start_x, start_y, end_x, end_y) = box.astype("int")

        return start_x, start_y, end_x, end_y


if __name__ == '__main__':
    man = ImageManager()
    image = cv2.imread('Images/cup-3.jpg')
    man.get_bounds(image)
