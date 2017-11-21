import json
import argparse
import os


class LabelMapManager:

    def __init__(self, label_map_path, object_list=None):
        self.label_map_path = label_map_path
        self.object_list = object_list

    def create_label_map(self):
        json_data = []
        if os.path.exists(self.label_map_path) is False:
            open(self.label_map_path, 'a')

        with open(self.label_map_path, 'w') as file:
            id_number = 1
            for object_name in  self.object_list:
                item = {'id': id_number, 'class': object_name}
                json_data.append(item)
                id_number += 1
            file.write(json.dumps(json_data, indent=4, sort_keys=False))
            file.close()

    def class_text_to_int(self, row_label):
        try:
            with open(self.label_map_path, 'r') as label_map:
                json_content = json.loads(label_map.read())
                for object in json_content:
                    if object['class'] == row_label:
                        return int(object['id'])
        except IOError as e:
            print(e)


def main():
    label_manager = LabelMapManager(FLAGS.label_map,FLAGS.objects)
    label_manager.create_label_map()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--label_map',
        type=str,
        default='Data/label_map.txt',
        help="""
           Path to the label_map file.
           """
    )
    parser.add_argument(
        '--objects',
        type=list,
        nargs='+',
        action='append',
        default=["cup", "water bottle", "ball", "bowl"],
        help="""
              Different objects that will be in the label_map.
              """
    )
    FLAGS = parser.parse_args()

    main()
