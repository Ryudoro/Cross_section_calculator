

def are_crosssection(slha_file, order):
    """
    Vérifie si les sections efficaces sont déjà écrites, et supprime
    également les doublons (smodels s'en charge mais c'est toujours mieux)
    """
    with open(slha_file, 'r') as f:
        data = f.readlines()
    test = True
    if data[-1]== " #no_cross-section" or data[-1]==" #no_cross-section\n":
        while test == True:
            if data[-2]== " #no_cross-section" or data[-2]==" #no_cross-section\n" or data[-3]==" #no_cross-section\n":
                data.pop()
                print(f'remove from {slha_file} a #no_cross-section"')
            else:
                test = False
        with open(slha_file, 'w') as f:
            for _ in data:
                f.write(_)
            return
    canaux = {}
    to_delete = []

    for i in range(len(data)):
        line = data[i]
        if line.startswith("XSECTION"):
            canal = (int(line.split(" ")[7]), int(line.split(" ")[8]),line.split(" ")[2])
            
            if canal in canaux:
                start = canaux[canal]
                end = start+1
                while not data[end].startswith('XSECTION'):
                    end+=1
                #end = start+order+3
                to_delete.extend(range(start, end))
            canaux[canal] = i
    lines = [line for i, line in enumerate(data) if i not in to_delete]

    with open(slha_file, 'w') as f:
        f.writelines(lines)
        
        
def canaux_finding(slha_file):
    
    with open(slha_file, 'r') as f:
        data = f.readlines()
        
    canaux = []

    for i in range(len(data)):
        line = data[i]
        if line.startswith("XSECTION"):
            if line.split(" ")[2] == '1.30E+04':
                canal = (int(line.split(" ")[7]), int(line.split(" ")[8]))
                canaux.append(canal)
    return canaux
