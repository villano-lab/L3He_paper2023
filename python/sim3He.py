import numpy as np
import pandas as pd
import scipy.interpolate as inter
import scipy.constants as co
import h5py

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
