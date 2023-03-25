from typing import *

import numpy as np
import pandas as pd

from model_util.response import A_cols

def interpolate(input_energy: float, energy: list, step_time: pd.DataFrame) -> List[float]:
    """interpolate between Beimer et al parameters, i.e. for any energy"""

    interp = []

    for col in A_cols:
        
        response = step_time[col].tolist()
        
        temp_result = np.interp(input_energy, energy, response)
        
        interp.append(temp_result)

    return interp

# #printing results
# print("\nResponses will be printed in parameter order [A1, A2, A3, A4, A5, A6, A7, A8, A9")
# print("A11, A12, A13, A14, A15, A16, A17, A18] Note there is no A10")
# print(f"\nThe response for {input_energy}keV with 3us shaping time is: \n")
# print(interp_3us)
# print(f"\nThe response for {input_energy}keV with 6us shaping time is: \n")
# print(interp_6us)
