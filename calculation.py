import math
from analyse_input import extract_m1_m2_mu
from analyse_input import extract_N1_N2_C1
from launcher import launcher
from are_already_cross_section import are_crosssection
#lien vers le dossier resummino local
resummino_bin = "./resummino-releases/bin/resummino"

#Choisir ici le fichier slha que l'on souhaite utiliser
# slha_file = "outputM_12000M_20mu100.slha"
# input_file = "ff1a240db6c1719fe9f299b3390d49d32050c4f1003286d2428411eca45bd50c.in"
# output_file = "output_file.txt"

# try :
#     m1,m2,mu = extract_m1_m2_mu(slha_file)
#     if m2>math.fabs(mu):
#         cas = 1
#     else:
#         cas = 2
# except :
#     N1,N2,C1 = extract_N1_N2_C1(slha_file)
#     #à ajouter: trouver si on a un scénario (N1,N2,C1) ou (N1,C1)

#     cas = 2

# if cas == 1:
#     particles = [(1000025,1000037), (1000025,-1000037), (-1000037,1000037)]
# if cas == 2:
#     particles = [(1000025,1000037), (1000025,-1000037), (-1000037,1000037), (1000023,1000035), (1000023,1000037), (1000023,-1000037)]

def one_slha_calculation(particles,input_file, slha_file, output_file, num_try, order):
    """
    Gestion du fichier log et lancement de la commande lancant Resummino
    """
    with open('log.txt', 'a') as f:
        f.write(f'{particles} cross-sections written in {slha_file}\n')
    if particles == None:
        with open(slha_file, 'a') as f:
            f.write(' #no_cross-section\n')

    #Utilisé ici pour vérifier si on a pas écrit 2 fois le #no_cross-section    
    are_crosssection(slha_file, order)
    if particles == None:
        return
    for particle_pair in particles:
        launcher(input_file, slha_file, output_file, particle_pair[0], particle_pair[1], num_try, order)