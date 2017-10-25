import argparse
import tensorflow as tf
import json
from image_manager import ImageManager

FLAGS = None

feature_name = [
    'width',
    'height',
    'xmin',
    'ymin',
    'xmax',
    'ymax',


]

PREDICTION_PATH = 'Data/predict_info.csv'

def input_fn_predict():

    def decode_data(line):
        parsed_line = tf.decode_csv(line, [[0], [0], [0.], [0.], [0.], [0.]])
        features = parsed_line
        return dict(zip(feature_name, features))

    dataset = (tf.contrib.data.TextLineDataset(PREDICTION_PATH)
               .skip(1)  # Skip header row
               .map(decode_data))  # Transform each elem by applying decode_csv fn
    dataset = dataset.batch(1)
    iterator = dataset.make_one_shot_iterator()
    next_feature_batch = iterator.get_next()
    return next_feature_batch, None


def predict():
    manager = ImageManager()
    manager.get_image_info([FLAGS.i], PREDICTION_PATH)

    feature_columns = [tf.feature_column.numeric_column(k) for k in feature_name]
    classifier = tf.estimator.DNNClassifier(
        feature_columns=feature_columns,
        hidden_units=[10, 10],
        n_classes=3,
        model_dir='train_model'
    )

    for predic in classifier.predict(input_fn=(lambda: input_fn_predict())):
        object_predict = find_object_by_id(predic['class_ids'])
        print(object_predict)


def find_object_by_id(predict_id):
    try:
        with open(FLAGS.label_map, 'r') as file:
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

    predict()

