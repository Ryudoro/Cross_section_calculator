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
  input_dir = "../../Parameters/Data"
  resummino_input = os.path.join(input_dir, "resummino_input")
  extract_softsusy_folder(os.path.join(input_dir, "slha_folder.tar"), os.path.join(input_dir, "slha_folder"))
  liste_input = os.listdir(input_dir)
  os.makedirs(resummino_input)
  for input in liste_input:
      particles = neutralino_choice(input)

def routine_creation():
  input_dir = "../../Parameters/Data"
  resummino_folder = os.path.join(input_dir, "resummino_input")
  extract_softsusy_folder(os.path.join(input_dir, "slha_folder.tar"), os.path.join(input_dir, "slha_folder"))
  liste_input = os.listdir(os.path.join(input_dir, "slha_folder"))
  os.makedirs(resummino_folder)
  tasks = []
  for input in liste_input:
      particles = neutralino_choice(os.path.join(input_dir, "slha_folder",input))
      particles = json.loads(particles)
      for particle_pair in particles["liste_particles"]:
        outgoing_particle_1 = particle_pair["outgoing_particle_1"]
        outgoing_particle_2 = particle_pair["outgoing_particle_2"]
        inpute = input.rstrip(".slha")
        resummino_input = f"resummino_{outgoing_particle_1}_{outgoing_particle_2}_{inpute}.in"
        modifie_outgoing_particles("resummino_modified.in", os.path.join(resummino_folder,resummino_input), outgoing_particle_1, outgoing_particle_2)
        modifie_slha_file(resummino_input, resummino_input, os.path.join("output_dir",input))
        output_resummino = os.makedirs(os.path.join(input_dir, "output_resummino",f"resummino_{outgoing_particle_1}_{outgoing_particle_2}_{inpute}.txt" ))
        tasks.append(resummino_input, output_resummino)
   return tasks

def run_resummino(input_file, output_file):
    #modifie_slha_file(input_file, slha_file)
    commande = f"{./../../../resummino-releases/bin/resummino} {input_file}"
    with open(output_file, 'w') as f:
        subprocess.run(commande, shell=True, stdout=f, text=True)
        
def routine_resummino():
  tasks = routine_creation()
  with ProcessPoolExecutor() as executor:
    futures = [executor.submit(run_resummino, *task) for task in tasks]
    for future in futures:
        future.result()
      
