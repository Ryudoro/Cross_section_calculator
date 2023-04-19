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
