import os
import json
from ancre_search import trouver_chemin_ancre

def modifie_json(keys_to_change, new_value):
    ancre = trouver_chemin_ancre("README.md")
    json_path = os.path.join(ancre,"core", "calculation", "infos.json")
    with open(json_path, 'r') as file:
        data = json.load(file)
    #print(os.path.join(ancre,"core", "calculation", "infos.json"))
    #data = json.loads(os.path.join(ancre,"core", "calculation", "infos.json"))
    data = data['evenements']
    print(data)

modifie_json(None,None)
