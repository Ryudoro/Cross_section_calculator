def finding_result(file, order):
  with open(input_file, 'r') as f:
    lines = f.readlines()

    for line in lines:
      _ = None
      if line.startswith(order+" ="):
        _ = line.split(" ")[2]
    return _
            
def writing_result(value, particle_1, particle_2):
  return f"XSECTION  1.30E+04  2212 2212 2 {particle_1} {particle_2} # 10000 events, [pb], pythia8 for LO
  0  0  0  0  0  0    {value} SModelSv2.2.1"

  
