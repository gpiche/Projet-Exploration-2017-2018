import cv2
import time as t
from predict import PredictionMaker
import os


class VideoManager:

    def __init__(self):
        self.prediction_maker = PredictionMaker()
        self.cap = cv2.VideoCapture(0)
        self.validate_cap(self.cap)

    @staticmethod
    def validate_cap(cap):
        if not cap.isOpened():
            print("Fatal Error: Could not open the specified file.")
            exit(-1)

    def read(self, object_to_predict):
        turn_time = 0
        while True:
            _, frame = self.cap.read()

            t.sleep(1)
            predict_object = self.predict(frame)

            if object_to_predict == predict_object:
                # call method to go to the object
                self.terminate_session()
                return "Object found !!! "
            elif turn_time == 3:
                self.terminate_session()
                return "Object not found..."
            else:
                pass
                turn_time += 1
                # rotate 45

    def terminate_session(self):
        self.cap.release()
        cv2.destroyAllWindows()

    def predict(self, frame):
        filename = "image_%0.5f.png" % t.time()
        cv2.imwrite(filename, frame)
        predicted_object = self.prediction_maker.predict(filename)
        os.remove(filename)
        return predicted_object

if __name__ == '__main__':
    video_manager = VideoManager()
    video_manager.read()