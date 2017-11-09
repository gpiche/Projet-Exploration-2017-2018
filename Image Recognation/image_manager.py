import pandas as pd
import cv2
import numpy as np



class ImageManager:

    def __init__(self):
        self.bounding_info = [1000, 1000, 0, 0]

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
        img = cv2.pyrDown(cv2.imread(image, cv2.IMREAD_UNCHANGED))

        ret, threshed_img = cv2.threshold(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY),
                                          127, 255, cv2.THRESH_BINARY)

        image, contours, hier = cv2.findContours(threshed_img, cv2.RETR_TREE,
                                                 cv2.CHAIN_APPROX_SIMPLE)
        height, width = img.shape[:2]
        for c in contours:
            x, y, w, h = cv2.boundingRect(c)
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

            if w == width and h == height and len(contours) > 1:
                pass
            elif w < width / 6 or h < height / 6:
                pass
            elif x > self.bounding_info[0] and y > self.bounding_info[1]:
                pass
            else:
                self.bounding_info = []
                self.bounding_info.extend([x, y, w, h])

            xmax = self.bounding_info[2] + self.bounding_info[0]
            ymax = self.bounding_info[3] + self.bounding_info[1]

            return self.bounding_info[0], self.bounding_info[1], xmax, ymax


if __name__ == '__main__':
    man = ImageManager()
    man.get_bounds('Images/ALL-69.jpg')
