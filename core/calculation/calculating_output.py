import subprocess
import sys
import os
from ancre_search import trouver_chemin_ancre

ancre = trouver_chemin_ancre("README.md") #C'est pour mon projet complet, pas besoin sinon
sys.path.append('ancre')

def extract_softsusy_folder(file, output_file):
  commande = f'tar -xzf {file}' #rajouter -C output_file si besoin
  subprocess.run(commande, shell=True, text=True)

def writing_result(infos):

  print(f"XSECTION  1.30E+04  2212 2212 2 {infos[2]} {infos[3]} # 10000 events, [pb], resummino for LO\n 0  0  0  0  0  0    {infos[4]} SModelSv2.2.1")


def caculation_result():
  outputs = os.listdir(os.path.join(ancre, "output_resummino")) #Chemin a modifier si dossier différent pour les fichiers .txt
  Infos = []
  for output in outputs:
    with open(os.path.join(ancre, "output_resummino",output), 'r') as f: #Chemin a modifier si dossier différent pour les fichiers .txt
      data = f.readlines()

    for i in range(len(data)):
      if "Results:" in data[i]:
        LO = data[i+1][:-1] #[:-1] pour enlever le \n
        NLO = data[i+2][:-1]
        NLL = data[i+3][:-1]
    _ = output.split("_")
    neutralino_1 = _[1]
    neutralino_2 = _[2]
    M_2 = _[-1].split("mu")[0][1:] #J'ajuste le split pour avoir uniquement la valeur qui m'intéresse
    mu = _[-1].split("mu")[1][:-4]
    Infos.append((M_2, mu,neutralino_1, neutralino_2, LO,NLO,NLL))
  return Infos

print(caculation_result())

