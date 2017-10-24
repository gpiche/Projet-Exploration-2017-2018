import os
import argparse
import glob
from image_manager import ImageManager

FLAGS = None


def main(image_manager):
    image_list = []
    image_directory_path = os.path.join(os.getcwd(), FLAGS.directory)

    for image in glob.glob(image_directory_path + '/*.jpg'):
        image_list.append(image)

    image_manager.get_image_info(image_list, 'Data/training_info.txt', index=FLAGS.index)

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
        '--index',
        type=str,
        default=1,
        help="""
          Class id of the object image directory.
          """
    )

    FLAGS = parser.parse_args()
    image_manager = ImageManager()
    main(image_manager)