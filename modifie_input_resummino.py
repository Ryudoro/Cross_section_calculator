
input_file = "ff1a240db6c1719fe9f299b3390d49d32050c4f1003286d2428411eca45bd50c.in"

def modifie_slha_file(file_before, file_after, slha_file):
    with open(file_before, 'r') as f:
        lines = f.readlines()

    with open(file_after, 'w') as f:
        for line in lines:
            if line.startswith("slha ="):
                line = f"slha = {slha_file}\n"
            f.write(line)

def modifie_outgoing_particles(input_file, output_file, new_particle1, new_particle2):
    with open(input_file, 'r') as f:
        lines = f.readlines()

    with open(output_file, 'w') as f:
        for line in lines:
            if line.startswith("particle1 ="):
                line = f"particle1 = {new_particle1}\n"
            elif line.startswith("particle2 ="):
                line = f"particle2 = {new_particle2}\n"
            f.write(line)
