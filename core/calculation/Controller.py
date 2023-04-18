import subprocess
import os
import json
import sys
sys.path.append('Cross_section_calculator')

from Parameters.File_creation.SLHA_input import extract_m1_m2_mu

def extract_softsusy_folder(file, outputfile):
  commande = f'tar -xzf {file} -C {outputfile}'
  
  
def is_there_folder(dossier):
  return os.path.isdir(dossier)
    
def parameter_study():
    param_study = []
    param_name = []
    with open('infos.json', 'r') as file:
        data = json.load(file)
        parameters = data['evenements'][1]['parametres']
    for param in list(parameters):
       if isinstance(parameters[param], dict):
          param_study.append({param :parameters[param]})
          param_name.append(param)
    return param_study,param_name
    
def neutralino_choice(file):
    m1,m2,mu = extract_m1_m2_mu(file)
    param_study, param_name = parameter_study()
    m2 = 1000
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
              
def routine():
  input_dir = ../../Parameters/Data
  extract_softsusy_folder(os.path.join(input_dir, "slha_folder.tar"), os.path.join(input_dir, "slha_folder"))
  liste_input = os.listdir(input_dir)
  for input in liste_input:
      particles = neutralino_choice(input)
      
