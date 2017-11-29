import os
from urllib.request import urlretrieve
import argparse
import numpy as np
import pandas as pd
import multiprocessing
from PIL import Image


args = None
MISSING_IMAGE_SHA1 = '6a92790b1c2a301c6e7ddef645dca1f53ea97ac2'


class DataAssembler:

    def __init__(self):
        self.current_directory = os.path.abspath(os.path.dirname(__file__))
        self.caffe_directory = os.path.abspath(os.path.join(self.current_directory, '../..'))
        self.training_directory = os.path.join(self.caffe_directory, 'data/image_recognition')

    def initialise_data(self, csv_file):
        csv_filename = os.path.join(self.current_directory, csv_file)
        df = pd.read_csv(csv_filename, index_col=None)
        df = df.iloc[np.random.permutation(df.shape[0])]
        if args.labels > 0:
            df = df.loc[df['label'] < args.labels]
        if args.images > 0:
            if args.images < df.shape[0]:
                df = df.iloc[:args.images]

        return df

    def get_files_name(self, df):
        images_directory = self.get_image_directory_path()
        self.create_work_directory(images_directory)

        df['image_filename'] = [
            os.path.join(images_directory, _.split('/')[-1]) for _ in df['image_name'] + '{}'.format('.jpeg')
        ]

    def get_image_directory_path(self):
        if self.training_directory is None:
            self.training_directory = os.path.join(self.caffe_directory, 'data\\image_recognition')
        return os.path.join(self.training_directory, 'images')

    @staticmethod
    def create_work_directory(images_directory):
        if not os.path.exists(images_directory):
            os.makedirs(images_directory)

    def download_images(self, df):
        num_workers = self.get_workers(args.workers)
        print('Downloading {} images with {} workers...'.format(
            df.shape[0], num_workers))
        pool = multiprocessing.Pool(processes=num_workers)
        map_args = zip(df['image_url'], df['image_filename'])
        return pool.map(self.download_image, map_args)

    def get_workers(self, num_workers):
        if num_workers <= 0:
            return multiprocessing.cpu_count() + num_workers

    def map_downloaded_data(self, df, results):
        df = df[results]
        for split in ['train', 'test']:
            split_df = df[df['_split'] == split]
            filename = os.path.join(self.training_directory, '{}.txt'.format(split))
            split_df = self.add_jpg_extension(split_df)
            split_df[['image_name', 'label']].to_csv(
                filename, sep=' ', header=None, index=None)
        print('Writing train/val for {} successfully downloaded images.'.format(
            df.shape[0]))

    def assemble_data_from_csv(self, csv_file):
        df = self.initialise_data(csv_file=csv_file)
        self.get_files_name(df)
        results = self.download_images(df)
        self.map_downloaded_data(df, results)

    @staticmethod
    def add_jpg_extension(df):
        for index in df['image_name'].index.tolist():
            df.loc[index, 'image_name'] = '{}'.format(df.loc[index, 'image_name'] + '.jpeg')
        return df

    @staticmethod
    def download_image(args_tuple):
        "For use with multiprocessing map. Returns filename on fail."
        try:
            url, filename = args_tuple
            if not os.path.exists(filename):
                urlretrieve(url, filename)
            test_read_image = Image.open(filename)
            return True
        except KeyboardInterrupt:
            raise Exception()  # multiprocessing doesn't catch keyboard exceptions
        except:
            return False


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Download a subset of Flickr Style to a directory')
    parser.add_argument(
        '-s', '--seed', type=int, default=0,
        help="random seed")
    parser.add_argument(
        '-i', '--images', type=int, default=-1,
        help="number of images to use (-1 for all [default])",
    )
    parser.add_argument(
        '-w', '--workers', type=int, default=-1,
        help="num workers used to download images. -x uses (all - x) cores [-1 default]."
    )
    parser.add_argument(
        '-l', '--labels', type=int, default=0,
        help="if set to a positive value, only sample images from the first number of labels."
    )

    args = parser.parse_args()
    np.random.seed(args.seed)

    assembler = DataAssembler()
    assembler.assemble_data_from_csv('Data/image_data.csv')



