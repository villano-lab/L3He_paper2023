import numpy as np
import pandas as pd
import scipy.interpolate as inter
import scipy.constants as co
import h5py

#get library path
import os.path
import sys
current_module = sys.modules[__name__]

mod_path = os.path.split(current_module.__file__)[0]

#a crude function to get liquid or gas density pressure (p) = None means liquid
def get3HeDensity(p=None):

  #got this from literature, see JURP paper.
  rholhe3 = 0.0792 #g/cm^3
  masshe3 = 3.01603 #molar mass
  nhe3 = (rholhe3/masshe3)*co.N_A

  if(p==None):
    return [rholhe3, nhe3]

  #pressure at room temp
  T=298 #K @ Room temp
  
  #1atm
  oneatm = co.value('standard atmosphere') #Pa
  
  #3He gas tubes 
  Pgas = oneatm
  ngas = Pgas*1e-6/(co.R*T)
  
  
  rhogas_mol = ngas
  rhogas = rhogas_mol*masshe3
  
  return [p*rhogas,p*ngas*co.N_A] 

def getSNOLABnFlux():
  fast_flux_df = pd.read_pickle('{}/data/FDF.txt'.format(mod_path)) # 'E' in MeV, 'spec' in neutrons cm^-2 sec^-1 MeV^-1
  print(fast_flux_df)

#some useful functions
def integrate_df(df):
  # (left-sided rectangular integral)
  dE = -df['E'].diff(periods = -1)
  dE.iat[-1] = dE.iat[-2]
  A = df['spec']*dE
  return A.sum()

def maxwell(E, B):
  # height of Maxwell distribution for energy E (eV) and temperature T (K) related to B via B = 1/kT
  return 2*B*np.sqrt(B*E/np.pi)*np.exp(-B*E)



