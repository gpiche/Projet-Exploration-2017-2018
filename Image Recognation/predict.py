import argparse
import tensorflow as tf
import json
from image_manager import ImageManager


class PredictionMaker:

    def __init__(self):
        self.feature_name = [
            'width',
            'height',
            'xmin',
            'ymin',
            'xmax',
            'ymax',
            'normalised_value'
        ]

        self.prediction_path = 'Data/predict_info.csv'
        self.label_map = 'Data/label_map.txt'

    def input_fn_predict(self):

        def decode_data(line):
            parsed_line = tf.decode_csv(line, [[0], [0], [0.], [0.], [0.], [0.], [0.]])
            features = parsed_line
            return dict(zip(self.feature_name, features))

        dataset = (tf.contrib.data.TextLineDataset(self.prediction_path)
                .skip(1)  # Skip header row
                .map(decode_data))  # Transform each elem by applying decode_csv fn
        dataset = dataset.batch(1)
        iterator = dataset.make_one_shot_iterator()
        next_feature_batch = iterator.get_next()
        return next_feature_batch, None

    def predict(self, image_path):
        manager = ImageManager()
        manager.get_image_info([image_path], self.prediction_path)

        feature_columns = [tf.feature_column.numeric_column(k) for k in self.feature_name]
        classifier = tf.estimator.DNNClassifier(
            feature_columns=feature_columns,
            hidden_units=[10, 10],
            n_classes=10,
            model_dir='/tmp/image_model'
        )

        predictions = classifier.predict(input_fn=(lambda: self.input_fn_predict()))

        for prediction in predictions:
            id = prediction['class_ids']
            if prediction['probabilities'][id] >= 0.6:
                object_predict = self.find_object_by_id(id)
                return object_predict
            else:
                return None

    def find_object_by_id(self, predict_id):
        try:
            with open(self.label_map, 'r') as file:
                json_content = json.loads(file.read())
                for object in json_content:
                    if object['id'] == predict_id:
                        return object['class']
        except IOError as e:
            print(e)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--i',
        type=str,
        default='Images/tasse-1.jpg',
        help="""
        Path to the image.
        """
    )

    parser.add_argument(
        '--label_map',
        type=str,
        default='Data/label_map.txt',
        help="""
        Path to the label map.
        """
    )
    FLAGS = parser.parse_args()

    pre = PredictionMaker()
    pre.predict('ball_0000.jpeg')





