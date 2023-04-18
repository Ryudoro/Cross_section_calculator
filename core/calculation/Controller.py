import subprocess
import os
import json
import sys
sys.path.append('Cross_section_calculator')

from Parameters.File_creation.SLHA_input import extract_m1_m2_mu

def extract_softsusy_folder(file, outputfile):
  commande = f'tar -xzf {file} -C {outputfile}
  
  
def is_there_folder(dossier):
  return os.path.isdir(dossier)
    
def neutralino_choice(file):
  m1,m2,mu = extract_m1_m2_mu(file)
  with open('infos.json', 'r') as file:
    data = json.load(file)
    parameters = data['evenements'][
    
  
