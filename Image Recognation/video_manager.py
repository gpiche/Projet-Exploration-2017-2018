import cv2
import time as t
from predict import PredictionMaker
import os



class VideoManager:

    def __init__(self):
        self.prediction_maker = PredictionMaker()
        self.cap = cv2.VideoCapture(0)
        self.validate_cap(self.cap)

    def validate_cap(self, cap):
        if not cap.isOpened():
            print("Fatal Error: Could not open the specified file.")
            exit(-1)

    def read(self):
        while True:
            _, frame = self.cap.read()

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            t.sleep(1)
            self.predict(frame)

            # Display the resulting frame
            #cv2.imshow('frame', gray)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()

    def predict(self, frame):
        filename = "image_%0.5f.png" % t.time()
        cv2.imwrite(filename, frame)
        self.prediction_maker.predict(filename)
        os.remove(filename)

if __name__ == '__main__':
    video_manager = VideoManager()
    video_manager.read()
