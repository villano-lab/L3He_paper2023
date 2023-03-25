import numpy as np
import scipy.integrate as integrate
from scipy import special
import pandas as pd


# creating parameters dictionary
A_cols: list = [
    f"A{i}"
    for i in range(1, 19)
    if i != 10
]

def response_function(E, En, data): 
    """defining the response function"""

    A1 = data[0]
    A2 = data[1]
    A3 = data[2]
    A4 = data[3]
    A5 = data[4]
    A6 = data[5]
    A7 = data[6]
    A8 = data[7]
    A9 = data[8]
    A11 = data[9]
    A12 = data[10]
    A13 = data[11]
    A14 = data[12]
    A15 = data[13]
    A16 = data[14]
    A17 = data[15]
    A18 = data[16]
    
    #ERFC 
    ERFC = 0.5*special.erfc(1-(((En+764)-E)/A3))
    #print(ERFC)
    
    #print(E)
    #print(En)
    normfac=5e3
    
    #filling delta values 
    delta1 = 0.0
    delta2 = 0.0 
    if(E <= (En + 764)):
        delta1 = 1
        delta2 = 0
    elif(E > (En + 764)):
        delta1 = 0
        delta2 = 1     
        
    #print(delta1,delta2).

    # print(f"""
    # E = {E}
    # A18 = {A18}
    # A13 = {A13}
    # A14 = {A14}
    # A15 = {A15}
    # (E-A18) = {(E-A18)}
    # (E-A13) = {(E-A13)}
    # (E-A18)/A15 = {(E-A18)/A15}
    # (E-A13)/A14 = {(E-A13)/A14}
    # """)

    junk1 = (E-A18)/A15
    junk2 = (E-A13)/A14

    if junk1 > 700 or junk2 > 700:
        print(f"you're gonna get an overflow for E = {E}!!!")
    
    T1 = (((A17*(E-A18))+A16)/(1+np.exp((E-A18)/A15)))
    T2 = (((A11*(A13-E)+A12))/(1+np.exp((E-A13)/A14)))
    T3 = (A6*(np.exp(-((En+764)-E)/A7))*ERFC)
    T4 = (A1*A4*(np.exp(-((En+764)-E)/A5))*ERFC)
    T5 = (delta1*A1*(np.exp(-0.5*((((En+764)-E)/A3))**2)))
    T6 = (delta2*A8*(np.exp(-0.5*(((E-(En+764))/A9))**2)))
    #print(T5*normfac,T6*normfac,E)
    response = T1+T2+T3+T4+T5+T6
    response*=normfac

    #+ (((A11*(A13-E)+A12))/(1+math.exp((E-A13)/A14))) + \
      #          (A6*(-math.exp(((En+764)-E)/A7))*ERFC) + (A1*A4*(-math.exp(((En+764)-E)/A5))*ERFC) + \
         #       (delta1*A1*(-math.exp(0.5*((En+764)-E)/A3)**2)) + (delta2*A8*(-math.exp(0.5*((En+764)-E)/A9)**2))

    return response


def solve_response(
        En: float,
        parameters: list,
        Emin: int,
        Emax: int,
        step: int,
    ):
    """solving response_function for energies in Emin - Emax range"""

    x_values = []
    y_values = []

    for energy in np.linspace(Emin, Emax, step):
        result = response_function(energy, En, parameters)
        x_values.append(energy)
        y_values.append(result)

    return x_values, y_values