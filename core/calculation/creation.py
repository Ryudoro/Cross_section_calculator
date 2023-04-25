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
  if True:
    extract_softsusy_folder(os.path.join(parameters_dir,'File_creation','SLHA_input', "softsusy_output.tar"), data_dir)
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
