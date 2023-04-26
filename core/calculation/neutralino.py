import json
import sys
import os
from ancre_search import trouver_chemin_ancre

ancre = trouver_chemin_ancre("README.md")
sys.path.append(ancre)

from Parameters.File_creation.SLHA_input.exctract_param import extract_m1_m2_mu

def parameter_study():
    param_study = []
    param_name = []
    json_path = os.path.join(ancre, 'core', 'calculation', 'infos.json')
    with open(json_path, 'r') as file:
        data = json.load(file)
        parameters = data['evenements'][1]['parametres']
    for param in list(parameters):
       if isinstance(parameters[param], dict):
          param_study.append({param :parameters[param]})
          param_name.append(param)
    return param_study,param_name

def neutralino_choice(file):
    json_path = os.path.join(ancre, 'core', 'calculation', 'infos.json')
    m1,m2,mu = extract_m1_m2_mu(file)
    param_study, param_name = parameter_study()
    if 'mu' and 'M2' in param_name:
       if float(m2) > float(mu):
          json_data = '{"liste_particles" : [{"outgoing_particle_1": 1000025, "outgoing_particle_2": 1000037}, {"outgoing_particle_1": 1000025, "outgoing_particle_2": -1000037}, {"outgoing_particle_1": -1000037, "outgoing_particle_2": 1000037}]}'
          data = json.loads(json_data)
          with open('particles.json', 'w') as file:
              json.dump(data, file)
          return json_data
       if float(m2) < float(mu):
          json_data = '{"liste_particles" : [{"outgoing_particle_1": 1000023, "outgoing_particle_2": 1000037}, {"outgoing_particle_1": 1000023, "outgoing_particle_2": -1000037}, {"outgoing_particle_1": 1000025, "outgoing_particle_2": 1000037}, {"outgoing_particle_1": 1000025, "outgoing_particle_2": -1000037}, {"outgoing_particle_1": -1000037, "outgoing_particle_2": 1000037}, {"outgoing_particle_1": 1000023, "outgoing_particle_2": 1000025}]}'
          data = json.loads(json_data)
          with open('particles.json', 'w') as file:
              json.dump(data, file)
          return json_data

