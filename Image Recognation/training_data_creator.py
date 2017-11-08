import os
import argparse
import glob
from image_manager import ImageManager
from label_map_manager import LabelMapManager



FLAGS = None


def main(image_manager):
    image_list = {}
    image_directory_path = os.path.join(os.getcwd(), FLAGS.directory)
    label_map_manager = LabelMapManager(FLAGS.path)

    for image in glob.glob(image_directory_path + '/*.jpg'):
        class_name = os.path.basename(image).split('-')[0]
        id = label_map_manager.class_text_to_int(class_name)
        image_list[image] = id

    image_manager.get_image_info(image_list, 'Data/training_info.csv', index=True)

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