import subprocess
import os

def extract_softsusy_folder(file, outputfile):
  commande = f'tar -xzf {file} -C {outputfile}
  
  
def is_there_folder(dossier):
  return os.path.isdir(dossier)
    
