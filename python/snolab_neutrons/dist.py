import numpy as np
import pandas as pd
import scipy.constants as co
import scipy.stats as ss
import itertools
import pickle
from scipy import signal

#matplotlib for plotting
import matplotlib as mpl
from matplotlib import pyplot as plt
plt.style.use('../mplstyles/stylelib/standard.mplstyle')

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

def extrapolate_snolab_flux(Ef,f,low=0.5e-6,high=2e-2,plot=False):

    #fast_lin_df = ffle[ffle < E_thresh]
    #fast_lin_df_spec = fflespec_smooth[ffle< E_thresh]
    Ef_trim = Ef[Ef<high]
    f_trim = f[Ef<high]
    fitted_line = ss.linregress(np.log(Ef_trim), np.log(f_trim))
    # return height of fitted loglog line, if energy is larger than thermal threshold

    func = lambda E: np.exp(fitted_line.intercept + fitted_line.slope*np.log(E))*(E > low)

    #plot if requested
    if plot:
       fig = plt.figure()
       ax = fig.add_subplot(111)
       ax.set_title('fit w/ points')
       ax.plot(Ef_trim, f_trim, 'o')
       ax.plot(Ef_trim, func(Ef_trim), linestyle = 'dashed')

    return func 

def read_snolab_HEflux(file='data/FDF.txt'):
    # read in fast neutron flux spectrum (from reading_n_spectra.ipynb)
    fast_flux_df = pd.read_pickle(file) # 'E' in MeV, 'spec' in neutrons cm^-2 sec^-1 MeV^-1

    #use numpy arrays
    ff = np.asarray(fast_flux_df['E']);
    ffspec = np.asarray(fast_flux_df['spec']);
    return ff,ffspec
