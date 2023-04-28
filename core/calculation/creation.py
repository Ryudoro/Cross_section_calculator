import json
import sys
import os
import subprocess
from ancre_search import trouver_chemin_ancre

ancre = trouver_chemin_ancre("README.md")
sys.path.append(ancre)
from Parameters.File_creation.Resumino_input.Outgoing_particles import modifie_outgoing_particles
from Parameters.File_creation.Resumino_input.slha_file_change import modifie_slha_file
from core.calculation.neutralino import neutralino_choice

def extract_softsusy_folder(file, outputfile):
  commande = f'tar -xzf {file} -C {outputfile}'
  subprocess.run(commande, shell=True, text=True)


def routine_creation():
  ancre = trouver_chemin_ancre("README.md")
  input_dir = os.path.join(ancre, "Parameters", "Data")
  resummino_folder = os.path.join(input_dir, "resummino_input")
  parameters_dir = os.path.join(ancre, "Parameters")
  data_dir = os.path.join(parameters_dir, 'Data')
  if not os.path.exists(os.path.join(data_dir,'output_dir')):
    extract_softsusy_folder(os.path.join(parameters_dir,'File_creation','SLHA_input', "softsusy_output.tar"), data_dir)
  liste_input = os.listdir(os.path.join(input_dir, "output_dir"))
  if not os.path.exists(resummino_folder):
    os.makedirs(resummino_folder)
  tasks = []
  for input in liste_input:
      #print(input)
      particles, type, m2, mu = neutralino_choice(os.path.join(input_dir, "output_dir",input))
      particles = json.loads(particles)
      for particle_pair in particles["liste_particles"]:
        outgoing_particle_1 = particle_pair["outgoing_particle_1"]
        outgoing_particle_2 = particle_pair["outgoing_particle_2"]
        inpute = input.rstrip(".slha")
        #print(inpute)
        resummino_input = f"resummino_{outgoing_particle_1}_{outgoing_particle_2}_{inpute}.in"
        if type:
          resummino_path = os.path.join(data_dir, 'output_resummino', 'm2_mu', f'output_{m2}_{mu}', resummino_input)
        else:
          resummino_path = os.path.join(data_dir, 'output_resummino','mu_m2', f'output_{m2}_{mu}', resummino_input)
          
        modifie_outgoing_particles(os.path.join(data_dir,"resummino_modified.in"), resummino_path, outgoing_particle_1, outgoing_particle_2)
        #file_path  = os.path.join(input_dir, "output_resummino",f"resummino_{outgoing_particle_1}_{outgoing_particle_2}_{inpute}.txt" )
        if type:
          file_path  = os.path.join(input_dir, "output_resummino", 'm2_mu', f'output_{m2}_{mu}',f"resummino_{outgoing_particle_1}_{outgoing_particle_2}_{inpute}.txt" )
        else:
          file_path  = os.path.join(input_dir, "output_resummino",'mu_m2', f'output_{m2}_{mu}',f"resummino_{outgoing_particle_1}_{outgoing_particle_2}_{inpute}.txt" )
        modifie_slha_file(resummino_path, resummino_path, os.path.join(data_dir,input))
        # if not os.path.exists(file_path):
        #   output_resummino = os.makedirs(file_path)
        tasks.append((resummino_path, file_path))
  return tasks
