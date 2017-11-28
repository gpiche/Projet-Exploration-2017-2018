from Protocol import Protocol
import json


class Protocol_json(Protocol):

    def process_query(self, query):
        query = json.loads(query)
        for key in query:
            if key == "salutation":
                return self.make_json_answer("Au nom du Peperoni, du fromage et de la sainte tomate je t'accorde cette pizza, AMEN!","reponse")


    def make_json_answer(self, answer, key):
        return json.dumps({key: answer})

    def make_list_answer(self, answer, tag, subtag):
        return json.dumps({tag: {subtag: [data for data in answer]}})
