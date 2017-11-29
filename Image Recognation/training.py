import argparse
import tensorflow as tf
import datetime
import time


FLAGS = None

feature_name = [
    'width',
    'height',
    'xmin',
    'ymin',
    'xmax',
    'ymax',
    'normalised_value'
]


def input_fn(file_path, perform_shuffle=False, repeat_count=1):

    def decode_csv(line):
        parsed_line = tf.decode_csv(line, [[0], [0], [0.], [0.], [0.], [0.], [0.], [0]])
        label = parsed_line[-1:]
        del parsed_line[-1:]
        features = parsed_line
        return dict(zip(feature_name, features)), label
    dataset = (tf.contrib.data.TextLineDataset(file_path)  # Read text file
               .skip(1)  # Skip header row
               .map(decode_csv))  # Transform each elem by applying decode_csv fn
    if perform_shuffle:
        # Randomizes input using a window of 256 elements (read into memory)
        dataset = dataset.shuffle(buffer_size=256)
    dataset = dataset.repeat(repeat_count)  # Repeats dataset this # times
    dataset = dataset.batch(32)  # Batch size to use
    iterator = dataset.make_one_shot_iterator()
    batch_features, batch_labels = iterator.get_next()
    return batch_features, batch_labels


def train():
    iteration = 1
    timeout = time.time() + 60 * 60 * 11

    feature_columns = [tf.feature_column.numeric_column(k) for k in feature_name]

    while True:
        tf.reset_default_graph()
        classifier = tf.estimator.DNNClassifier(
            feature_columns=feature_columns,
            hidden_units=[10, 10],
            n_classes=10,
            model_dir='/tmp/image_model'
        )

        print("[INFO] Training.... ")
        classifier.train(
            input_fn=lambda: input_fn(FLAGS.training_dataset, True, 100))

        print("[INFO] Evaluating.... ")
        evaluate_result = classifier.evaluate(
            input_fn=lambda: input_fn(FLAGS.training_dataset, False, 4))
        print("[INFO] ---------------------------------------")

        for key in evaluate_result:
            print("   {}, was: {} \n".format(key, evaluate_result[key]))

        iteration += 1


def main():
    if not tf.gfile.Exists(FLAGS.training_dataset):
        tf.logging.fatal('File does not exist %s', FLAGS.training_dataset)

    train()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--label_map',
        type=str,
        default='',
        help="""
        Path to the label map.
        """
    )
    parser.add_argument(
        '--training_dataset',
        type=str,
        default=r'C:\Users\Guillaume\Documents\Automne 2017\Exploration nouvelle technologie\Projet-Exploration-2017-2018\Image Recognation\Data\training_info.csv',
        help="""
        Path to the dataset.
        """
    )
    FLAGS = parser.parse_args()
    main()