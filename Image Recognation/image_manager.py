import pandas as pd
import cv2


class ImageManager:

    def __init__(self):
        self.bounding_info = {}

    def get_image_info(self, image_paths, output_path, index=None):
        value_list = []
        for image in image_paths:
            img = cv2.imread(image, 1)
            height, width = self.get_size(img)
            xmin, ymin, xmax, ymax = self.get_bounds(img)
            value = (width, height, xmin, ymin, xmax, ymax)
            if index is not None:
                value += (index,)
            value_list.append(value)

        self.create_csv_file(output_path, index, value_list)

    def create_csv_file(self, output_path, index, value_list):
        if index is None:
            column_name = ['width', 'height', 'xmin', 'ymin', 'xmax', 'ymax']
        else:
            column_name = ['width', 'height', 'xmin', 'ymin', 'xmax', 'ymax', 'class_id']

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
