import os
import subprocess
from modifie_input_resummino import modifie_slha_file
from modifie_input_resummino import modifie_outgoing_particles
from analyse_output import write_in_slha
from are_already_cross_section import are_crosssection
from are_already_cross_section import canaux_finding

resummino_bin = "./resummino-3.1.2/bin/resummino"
# slha_file = "outputM_12000M_20mu100.slha"
# input_file = "ff1a240db6c1719fe9f299b3390d49d32050c4f1003286d2428411eca45bd50c.in"
# output_file = "output_file.txt"

# particle_1 = "1000024"
# particle_2 = "-1000024"

def launch_command(resummino_bin,input_file, output_file, order):
    """
    Lance la commande pour resummino, pour modifier l'emplacement de resummino
    il faut préciser le resummino_bin.
    """
    if order == 0:
        commande = f"{resummino_bin} {input_file} --lo"
    if order == 1:
        commande = f"{resummino_bin} {input_file} --nlo"
    if order == 2:
        commande = f"{resummino_bin} {input_file}"

    with open(output_file, 'w') as f:
        subprocess.run(commande, shell=True, stdout=f, text=True)



def launcher(input_file, slha_file, output_file, particle_1, particle_2, num_try, order):
    #modifie_slha_file(input_file, input_file, slha_file)
    modifie_outgoing_particles(input_file, input_file, particle_1, particle_2)
    #on lance si c'est le premier essai par défaut
    
    hist = 0
    already_written_canal = canaux_finding(slha_file)
    
    if (particle_1, particle_2) in already_written_canal:
        return
    
    if num_try == 0:
        launch_command(resummino_bin, input_file, output_file, order)

    #Ici on écrit dans le fichier slha, la variable hist permet de voir s'il y a eu une erreur
    #Dans le calcul des section efficaces Lo et NLO
        hist = write_in_slha(output_file, slha_file, order, particle_1, particle_2, 'all')

    #On vérifie si jamais on a écrit trop de choses
    are_crosssection(slha_file, order)

    #Si jamais il y a effectivement une erreur, on l'indique et on relance avec cette fois num_try = 0
    if hist == 1:
        print("error")
        num_try = 0
        modifie_outgoing_particles(input_file, input_file, particle_1, particle_2)
        launcher(input_file, slha_file, output_file, particle_1, particle_2, num_try, order)
#launcher(input_file, slha_file, output_file, particle_1, particle_2)
