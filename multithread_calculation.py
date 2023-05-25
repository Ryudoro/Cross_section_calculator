import subprocess
import os
from concurrent.futures import ProcessPoolExecutor
from calculation import one_slha_calculation
from modifie_input_resummino import modifie_slha_file
from particles_discrim import discrimination_particles

def routine_creation(order, slha_folder_name):
   #slha_file = "outputM_12000M_20mu100.slha"
    #Fichier d'input de resummino de référence
    input_file = "ff1a240db6c1719fe9f299b3390d49d32050c4f1003286d2428411eca45bd50c.in"

    #Ne fait rien
    output_file = "output_file.txt"

    #Listes des differents fichiers sur lesquels faire tourner le logiciel
    Liste_slha = []
    Liste_resummino_in = []
    Liste_output_file = []
    Liste_particles = []
    Liste = []

    #Vérification des dossiers d'entrée et sortie de Resummino
    if not os.path.exists('resummino_in'):
        os.mkdir('resummino_in')
    if not os.path.exists('resummino_out'):
        os.mkdir('resummino_out')

    #On créer la liste des fichiers d'entrée
    liste_slha = os.listdir(slha_folder_name)

    #ancre
    pwd = os.getcwd()

    #Utilisation chemin absolu (à privilégier)
    slha_folder = os.path.join(pwd, slha_folder_name)

    #a = nombre fichiers, b = nombre fichiers déjà écris, c = nombre fichiers déjà ignorés
    a,b,c = 0,0,0

    #Boucle sur tous les fichiers, dans l'ordre de listdir (ordre +/- aléatoire)
    for slha in liste_slha:

        slha_path = os.path.join(slha_folder,slha)
        #Variable utilisée pour éviter les abérations (grosse différence LO/NLO)
        num_try = 0
        with open(slha_path, 'r') as f:
            data = f.readlines()
            a+=1
            
        if data[-1].endswith("Resumminov3.1.2\n") or data[-1].endswith("Resumminov3.1.2"):
            b+=1
            #On augmente cette variable de 1, comme ca si elle est > 0 on ne refait pas le calcul
            num_try+=1
        elif data[-1].endswith(" #no_cross-section\n") or data[-1].endswith(" #no_cross-section"):
            c+=1
            #On augmente cette variable de 1, comme ca si elle est > 0 on ne refait pas le calcul
            num_try+=1

        #on enlève le .slha
        slha_file_name = slha[6:-5]

        #On prend le fichier de référence, et on créer une copie dans resummino_in avec le bon fichier slha
        modifie_slha_file(input_file, f"resummino_in/resummino_{slha_file_name}.in",slha_path)

        #On ajoute les noms à la liste (in, out et slha)
        Liste_resummino_in.append(f"resummino_in/resummino_{slha_file_name}.in")
        Liste_output_file.append(f"resummino_out/resummino_out_{slha_file_name}.txt")
        Liste_slha.append(slha_path)

        #On liste ici les canaux à utiliser, si scénario exclu alors renvoi None
        particles = discrimination_particles(slha_path)
        Liste_particles.append(particles)

        #On pourrait optimiser en enlevant les variables qui ne changent pas d'une itération à l'autre
        #Mais ce n'est pas très important (négligeable niveau temps de compilation comparé à Resummino)
        Liste.append((particles, f"resummino_in/resummino_{slha_file_name}.in", slha_path, f"resummino_out/resummino_out_{slha_file_name}.txt", num_try, order))
    print(f" Number of files created : {a-b-c}")
    return Liste

def routine_resummino(order, slha_folder_name):
  
  #On créer la liste
  tasks = routine_creation(order, slha_folder_name)

  #On lance le programme avec les performances maximales, à changer si besoin
  with ProcessPoolExecutor() as executor:
    futures = [executor.submit(one_slha_calculation, *task) for task in tasks]
    for future in futures:
        future.result()

#Modifie ici, 1er paramètre pour l'ordre du calcul (0,1 ou 2) et deuxième pour ton dossier slha
routine_resummino(1, 'exemple')
