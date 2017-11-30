import json
from video_manager import VideoManager


class ProtocolJson:

    def __init__(self):
        self.video_manager = VideoManager()

    def process_query(self, query):
        query = json.loads(query)
        for key in query:
            if key == "object":
                return self.video_manager.read(query[key])
            elif key == "command":
                if query[key] == "go_ahead":
                    pass
                    # call go_ahead method
                elif query[key] == "go_back":
                    pass
                    # call go_back method
                elif query[key] == "go_right":
                    pass
                    # call go_right method
                elif query[key] == "go_left":
                    pass
                    # call go_left method
                elif query[key] == "stop":
                    pass
                    # call stop method

    @staticmethod
    def make_json_answer(answer, key):
        return json.dumps({key: answer})

    @staticmethod
    def make_list_answer(answer, tag, subtag):
        return json.dumps({tag: {subtag: [data for data in answer]}})
