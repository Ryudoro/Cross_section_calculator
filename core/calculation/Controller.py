import subprocess
import os
import json
import sys
import subprocess
from concurrent.futures import ProcessPoolExecutor
import tempfile
from ancre_search import trouver_chemin_ancre

ancre = trouver_chemin_ancre("README.md")
sys.path.append(ancre)

from Parameters.File_creation.SLHA_input.exctract_param import extract_m1_m2_mu
from core.calculation.creation import routine_creation


  
  
def is_there_folder(dossier):
  return os.path.isdir(dossier)
    
# def parameter_study():
#     param_study = []
#     param_name = []
#     with open('infos.json', 'r') as file:
#         data = json.load(file)
#         parameters = data['evenements'][1]['parametres']
#     for param in list(parameters):
#        if isinstance(parameters[param], dict):
#           param_study.append({param :parameters[param]})
#           param_name.append(param)
#     return param_study,param_name
    
# def neutralino_choice(file):
#     m1,m2,mu = extract_m1_m2_mu(file)
#     param_study, param_name = parameter_study()
#     m2 = 1000
#     if 'mu' and 'M2' in param_name:
#        if float(m2) > float(mu):
#           json_data = '{"liste_particles" : [{"outgoing_particle_1": 1000025, "outgoing_particle_2": 1000037}, {"outgoing_particle_1": 1000025, "outgoing_particle_2": -1000037}, {"outgoing_particle_1": -1000037, "outgoing_particle_2": 1000037}]}'
#           data = json.loads(json_data)
#           with open('particles.json', 'w') as file:
#               json.dump(data, file)
#           return json_data
#        if float(m2) < float(mu):
#           json_data = '{"liste_particles" : [{"outgoing_particle_1": 1000023, "outgoing_particle_2": 1000037}, {"outgoing_particle_1": 1000023, "outgoing_particle_2": -1000037}, {"outgoing_particle_1": 1000025, "outgoing_particle_2": 1000037}, {"outgoing_particle_1": 1000025, "outgoing_particle_2": -1000037}, {"outgoing_particle_1": -1000037, "outgoing_particle_2": 1000037}, {"outgoing_particle_1": 1000023, "outgoing_particle_2": 1000025}]}'
#           data = json.loads(json_data)
#           with open('particles.json', 'w') as file:
#               json.dump(data, file)
#           return json_data
              
# def routine():
#   input_dir = "../../Parameters/Data"
#   resummino_input = os.path.join(input_dir, "resummino_input")
#   extract_softsusy_folder(os.path.join(input_dir, "slha_folder.tar"), os.path.join(input_dir, "slha_folder"))
#   liste_input = os.listdir(input_dir)
#   os.makedirs(resummino_input)
#   for input in liste_input:
#       particles = neutralino_choice(input)


def run_resummino(input_file, output_file):
    #modifie_slha_file(input_file, slha_file)
    _ = ancre.split("/")
    ancre_2 = '/'.join(_[:-1])
    chemin = os.path.join(ancre_2, "resummino-releases/bin/resummino")
    commande = f"python3 {chemin} {input_file}"
    with open(output_file, 'w') as f:
        subprocess.run(commande, shell=True, stdout=f, text=True)
        
def routine_resummino():
  tasks = routine_creation()
  with ProcessPoolExecutor() as executor:
    futures = [executor.submit(run_resummino, *task) for task in tasks]
    for future in futures:
        future.result()
      
