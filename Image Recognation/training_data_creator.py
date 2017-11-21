import os
import argparse
from image_manager import ImageManager
import cv2




FLAGS = None
current_directory = os.path.abspath(os.path.dirname(__file__))
caffe_directory = os.path.abspath(os.path.join(current_directory, '../..'))
training_directory = os.path.join(caffe_directory, 'data/image_recognition')
image_directory = os.path.join(training_directory, 'images')


def main(image_manager):
    image_list = {}

    training_mapping_file = os.path.join(training_directory, 'train.txt')

    with open(training_mapping_file) as file:
        for line in file.readlines():
            image_name = line[:-3]
            image = os.path.join(image_directory, image_name)
            is_valid(image)
            id = line[-3:].rstrip('\n')
            if is_valid(image):
                image_list[image] = id

    image_manager.get_image_info(image_list, 'Data/training_info.csv', index=True)


def is_valid(image):
    read_test = cv2.imread(image)
    if read_test is None:
        return False
    return True

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--directory',
        type=str,
        default='Images',
        help="""
        Path to the images folder.
        """
    )

    parser.add_argument(
        '--path',
        type=str,
        default='Data/label_map.txt',
        help="""
              Path to the label_map file.
              """
    )

    FLAGS = parser.parse_args()
    image_manager = ImageManager()
    main(image_manager)