import math

def search_in_output(output_file):
    Infos = []
    with open(output_file, 'r') as f: #Chemin a modifier si dossier différent pour les fichiers .txt
        data = f.readlines()
    for i in range(len(data)):
        if "Results:" in data[i]:
            LO = data[i+1][:-1] #[:-1] pour enlever le \n
            NLO = data[i+2][:-1]
            NLL = data[i+3][:-1]
            Infos.append((LO,NLO,NLL))
    return Infos[0]

def writing_result(value, particle_1, particle_2, slha_file, order, type_writing):
  with open(slha_file, 'a') as f:
    if type_writing == 'all':
        f.write(f"\nXSECTION  1.30E+04  2212 2212 2 {particle_1} {particle_2} # [pb] \n")
        for i in range(order+1):
            f.write(f" 0  0  {i}  0  0  0    {value[i]} Resumminov3.1.2\n")
    if type_writing == 'max':
        f.write(f"\nXSECTION  1.30E+04  2212 2212 2 {particle_1} {particle_2} # [pb] \n 0  0  {order}  0  0  0    {value} Resumminov3.1.2\n")
def write_in_slha(output_file, slha_file, order, particle_1, particle_2, type_writing):
    results = search_in_output(output_file)
    if type_writing == 'max':
        if order == 0:
            result = results[0].split(" ")[2][1:]
        elif order == 1:
            result = results[1].split(" ")[2][1:]
        elif order == 2:
            result = results[2].split(" ")[2][1:]
    if type_writing == "all":
        result = [results[0].split(" ")[2][1:], results[1].split(" ")[2][1:], results[2].split(" ")[2][1:]]
    
    if order == 1:
        #_ = math.fabs(results[0].split(" ")[2][1:]-results[1].split(" ")[2][1:])
        if float(results[1].split(" ")[2][1:])>2*float(results[0].split(" ")[2][1:]) or float(results[0].split(" ")[2][1:])> 2* float(results[1].split(" ")[2][1:]):
            with open('log.txt', 'a') as f:
                f.write(f"to much change between LO and NLO for {particle_1} and {particle_2} with {slha_file}")
            return 1
    writing_result(result, particle_1, particle_2, slha_file, order, type_writing)
    return 0