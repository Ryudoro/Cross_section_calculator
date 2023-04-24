import os

def trouver_chemin_ancre(critere, chemin_courant=None):
    if chemin_courant is None:
        chemin_courant = os.path.abspath(os.path.dirname(__file__))
    
    while True:
        if critere in os.listdir(chemin_courant):
            return chemin_courant
        else:
            nouveau_chemin = os.path.dirname(chemin_courant)
            if nouveau_chemin == chemin_courant:
                # Nous avons atteint la racine du système de fichiers sans trouver le critère
                raise ValueError(f"Le critère '{critere}' n'a pas été trouvé dans l'arborescence du système de fichiers.")
            chemin_courant = nouveau_chemin

