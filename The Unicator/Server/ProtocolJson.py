import json
#from video_manager import VideoManager
from Robot import Robot

class ProtocolJson:

    LEFT_TRIM = 0
    RIGHT_TRIM = 0

    def __init__(self):
        pass
        #self.video_manager = VideoManager()
        #self.robot = Robot(ProtocolJson.LEFT_TRIM,ProtocolJson.RIGHT_TRIM)

    def process_query(self, query):
        query = json.loads(query)
        for key in query:
            if key == "object":
                print(query[key])
                #return self.video_manager.read(query[key])
            elif key == "command":
                if query[key] == "go_ahead":
                    print("Ahead")
                    robot.forward(100)
                elif query[key] == "go_back":
                    print ("Back")
                    robot.backward(100)
                elif query[key] == "go_right":
                    print ("Right")
                    robot.right(100)
                elif query[key] == "go_left":
                    print ("Left")
                    robot.left(100)
                elif query[key] == "stop":
                    print("Stopped !")
                    robot.stop()

    @staticmethod
    def make_json_answer(answer, key):
        return json.dumps({key: answer})

    @staticmethod
    def make_list_answer(answer, tag, subtag):
        return json.dumps({tag: {subtag: [data for data in answer]}})
