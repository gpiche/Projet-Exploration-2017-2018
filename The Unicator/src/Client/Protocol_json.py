from Protocol import Protocol
import json
import os


class Protocol_json(Protocol):
    """Interface du langage de communication JSON"""
    key = ''

    def __init__(self):
        super(Protocol_json, self).__init__()

    def verify_connexion(self, tag):
        self.key = "salutation"
        return json.dumps({self.key: tag})

    def know_server_name(self, tag):
        self.key = "nomServeur"
        return json.dumps({"action": tag})


    def close_connexion(self, tag):
        self.key = "reponse"
        return json.dumps({"action": tag})

    def process_answer(self, answer):
        json_answer = json.loads(answer)

        try:
            json_answer[self.key]
        except:
            self.key = "reponse"

        if json_answer[self.key] == "bonjourClient":
            return "Oui"
        elif "dossier" in json_answer[self.key]:
            return self.obtain_data(json_answer[self.key], "dossier")
        elif "fichier" in json_answer[self.key]:
            return self.obtain_data(json_answer[self.key], "fichier")

        return json_answer[self.key]

    def obtain_data(self, json_answer, tag):
        answer = ''
        for data in json_answer[tag]:
            answer += data + '/'
        return answer
