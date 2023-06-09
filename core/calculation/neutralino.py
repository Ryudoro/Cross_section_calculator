import json
import math
import sys
import os
import shutil
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
       if float(m2) >= math.fabs(float(mu)):
            path = os.path.join(ancre, 'Parameters', 'Data', 'output_resummino', 'm2>mu', f'output_{m2}_{mu}')
            old_path = os.path.join(ancre, 'Data', 'output_dir', file)
            print(path, old_path)
            if not os.path.exists(path):
                os.makedirs(path)
            shutil.copy(old_path, os.path.join(path, file +'_'))
            json_data = '{"liste_particles" : [{"outgoing_particle_1": 1000025, "outgoing_particle_2": 1000037}, {"outgoing_particle_1": 1000025, "outgoing_particle_2": -1000037}, {"outgoing_particle_1": -1000037, "outgoing_particle_2": 1000037}]}'
            data = json.loads(json_data)
            with open('particles.json', 'w') as file:
                json.dump(data, file)
            return json_data, True, m2,mu
       if float(m2) < math.fabs(float(mu)):
            path = os.path.join(ancre, 'Parameters',  'Data', 'output_resummino', 'm2<mu', f'output_{m2}_{mu}')
            old_path = os.path.join(ancre, 'Data', 'output_dir', file)
            if not os.path.exists(path):
                os.makedirs(path)
            shutil.copy(old_path, os.path.join(path, file +'_'))
            json_data = '{"liste_particles" : [{"outgoing_particle_1": 1000023, "outgoing_particle_2": 1000037}, {"outgoing_particle_1": 1000023, "outgoing_particle_2": -1000037}, {"outgoing_particle_1": 1000025, "outgoing_particle_2": 1000037}, {"outgoing_particle_1": 1000025, "outgoing_particle_2": -1000037}, {"outgoing_particle_1": -1000037, "outgoing_particle_2": 1000037}, {"outgoing_particle_1": 1000023, "outgoing_particle_2": 1000025}]}'
            data = json.loads(json_data)
            with open('particles.json', 'w') as file:
                json.dump(data, file)
            return json_data, False, m2, mu

