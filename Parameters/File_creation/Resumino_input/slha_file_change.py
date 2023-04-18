def modifie_slha_file(input_file, output_file, slha_file):
    with open(input_file, 'r') as f:
        lines = f.readlines()

    with open(output_file, 'w') as f:
        for line in lines:
            if line.startswith("slha ="):
                line = f"slha = {slha_file}\n"
            f.write(line)
