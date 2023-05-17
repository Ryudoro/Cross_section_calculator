import math
from analyse_input import extract_m1_m2_mu
from analyse_input import extract_N1_N2_C1

#Choisi ici les canaux que tu souhaites utiliser
def discrimination_particles(slha_file):
    """
    Choix des différents canaux et conditions sur les calculs de sections efficaces
    pour l'instant C1<92 or N1>600 or C2>1200
    """
    m1,m2,mu = extract_m1_m2_mu(slha_file)
    N1,N2,C1,C2 = extract_N1_N2_C1(slha_file)
    abs_mu = math.fabs(mu)
    if C1<92 or N1>600 or C2>1200:
        return None
    if m2>=abs_mu:
        return [(1000025,1000037),(1000025,-1000037), (-1000037, 1000037)]
    elif m2<abs_mu:
        return [(1000023,1000037), (1000023,-1000037), (1000025, 1000037), (1000025, -1000037), (-1000037,1000037), (1000023,1000025)]
    
