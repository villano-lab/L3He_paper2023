from typing import *

import pandas as pd

def load_parameters(fname: str, colname: str = 'Energy [keV]') -> Tuple[pd.DataFrame, list]:
    """returns dataframe from file and `Energy [keV]` column as list"""
    data = pd.read_csv(fname)
    energy_col = data[colname].tolist()

    return data, energy_col

def load_specific_row(
        fname: str,
        value: float,
        colname: str = 'Energy [keV]',
    ) -> Tuple[float, dict]:
    """loads specific row from the csv at `fname`"""

    df: pd.DataFrame = pd.read_csv(fname)

    df_filtered: pd.DataFrame = df.loc[df[colname] == value]

    print(df_filtered)

    if len(df_filtered) != 1:
        if len(df_filtered) > 1:
            raise KeyError(f"""found more than one row with value {value} at column {colname}
            {str(df_filtered)}
            """)
        else:
            raise KeyError(f"""couldn't find any rows with value {value} at column {colname}""")

    output: dict = dict(df_filtered.to_dict(orient='records')[0])
    return (output[colname], output)
        




