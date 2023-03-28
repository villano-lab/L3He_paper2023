import numpy as np
import pandas as pd
import scipy.constants as co
import scipy.stats as ss
import itertools
import pickle
from scipy import signal

# constants
snothermal = 4144.9/10000/86400

import prob_util.int_dis as dist 

def get_thermal(B):
    func = lambda E: dist.maxwell(E,B) 
    return func

def get_snolab_thermal(B):
    func = lambda E: snothermal*dist.maxwell(E,B) 
    return func

def smooth_snolab_HEflux(cutoff=0.3,file='data/FDF.txt'):

    Eff,ff = read_snolab_HEflux(file)
    Eff_trim = Eff[Eff>cutoff]
    ff_trim = ff[Eff>cutoff]

    #smooth the data
    ff_smooth = signal.savgol_filter(ff_trim, 2001, 3) # window size 1001, polynomial order 3
    return Eff_trim,ff_smooth

def smooth_snolab_LEflux(cutoff=0.3,file='data/FDF.txt'):

    Eff,ff = read_snolab_HEflux(file)
    Eff_trim = Eff[Eff<=cutoff]
    ff_trim = ff[Eff<=cutoff]

    #smooth the data
    ff_smooth = signal.savgol_filter(ff_trim, 75, 3) # window size 75, polynomial order 3
    return Eff_trim,ff_smooth

def read_snolab_HEflux(file='data/FDF.txt'):
    # read in fast neutron flux spectrum (from reading_n_spectra.ipynb)
    fast_flux_df = pd.read_pickle(file) # 'E' in MeV, 'spec' in neutrons cm^-2 sec^-1 MeV^-1

    #use numpy arrays
    ff = np.asarray(fast_flux_df['E']);
    ffspec = np.asarray(fast_flux_df['spec']);
    return ff,ffspec
