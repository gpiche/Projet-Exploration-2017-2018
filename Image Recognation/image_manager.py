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
            xmin, ymin, xmax, ymax = self.get_bounds(image)
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
        image = cv2.imread(image)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # grayscale
        _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)  # threshold
        kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
        dilated = cv2.dilate(thresh, kernel, iterations=13)  # dilate
        _, contours, hierarchy = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)  # get contours

        # for each contour found, draw a rectangle around it on original image
        x , y , w, h = 0, 0, 0, 0
        for contour in contours:
            # get rectangle bounding contour
            [x, y, w, h] = cv2.boundingRect(contour)

            # discard areas that are too large
            if h > 400 and w > 400:
                continue

            # discard areas that are too small
            if h < 40 or w < 40:
                continue

            # draw rectangle around contour on original image
        return x, y, w, h





if __name__ == '__main__':
    man = ImageManager()
    man.get_bounds('Images/ALL-69.jpg')
