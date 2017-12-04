from time import sleep
from TestConnexion import Connexion
import json


client = Connexion()

client.send(json.dumps({'command': 'go_ahead'}))
sleep(2)

client.send(json.dumps({'command': 'go_back'}))
sleep(2)

client.send(json.dumps({'object': 'cup'}))
sleep(2)

client.send(json.dumps({'command': 'stop'}))
sleep(2)

client.close()