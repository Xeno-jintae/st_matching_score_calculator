from typing import Dict
from typing import List
import pandas as pd
from pandas import DataFrame

from calculator import calculate_bvalues_simulation as CBS
from calculator import calculate_risky_weight_scores as CRW

def calculate_score(dic_ib : Dict, dic_rw : Dict) -> DataFrame:
    matching_scores = []

    bvalue_rate = 0.3
    job_rate = 1 - bvalue_rate

    for wrap_product, value in dic_ib.items():
        matching_score = bvalue_rate * value + job_rate * dic_rw[wrap_product]
        matching_scores.append({'wrapProductNo' : wrap_product, 'matchingScore' : matching_score})

    df = pd.DataFrame(matching_scores).sort_values(['matchingScore'], ascending=False)
    df['rank'] = df['matchingScore'].rank(ascending=False, method='min')

    return df

def calculate_wrap(df1 : DataFrame, df2 : DataFrame, wrap_list :List, period :int, z_value : float, job_code : str, age : int) -> DataFrame:
    dic_ib = CBS.get_inv_sim_bvalues(df1, wrap_list, period, z_value)
    dic_rw = CRW.get_risky_weight_score(df2, wrap_list, job_code, age)

    return calculate_score(dic_ib, dic_rw)