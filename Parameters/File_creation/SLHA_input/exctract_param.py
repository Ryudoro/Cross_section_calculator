import pyslha

def extract_m1_m2_mu(file_path):
     
     data = pyslha.read(file_path)

     m1 = data.blocks['EXTPAR'][1]
     m2 = data.blocks['EXTPAR'][2]
     mu = data.blocks['EXTPAR'][23]

     result = {
          'M_1(MX)': m1,
          'M_2(MX)': m2,
          'mu(MX)' : mu
     }

     return m1,m2,mu
