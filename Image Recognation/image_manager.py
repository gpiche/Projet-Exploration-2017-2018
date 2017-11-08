import pandas as pd
import cv2
import numpy as np



class ImageManager:

    def __init__(self):
        self.bounding_info = {}

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

    def create_csv_file(self, output_path, index, value_list):
        if index is False:
            column_name = ['width', 'height', 'xmin', 'ymin', 'xmax', 'ymax', 'normalised_value']
        else:
            column_name = ['width', 'height', 'xmin', 'ymin', 'xmax', 'ymax', 'normalised_value', 'class_id']

        xml_df = pd.DataFrame(value_list, columns=column_name)
        xml_df.to_csv(output_path, index=None)

    def get_size(self, img):
        return img.shape[:2]

    def get_bounds(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # grayscale
        _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)  # threshold
        kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
        dilated = cv2.dilate(thresh, kernel, iterations=13)  # dilate
        _, contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)  # get contours

        # for each contour found, draw a rectangle around it on original image
        x, y, w, h = 0, 0, 0, 0
        for contour in contours:

            [x, y, w, h] = cv2.boundingRect(contour)

            if h > 1500 and w > 1500:
                continue

            if h < 250 or w < 250:
                continue

        return x, y, w, h



if __name__ == '__main__':
    pass
