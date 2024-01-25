from pandas import DataFrame
from typing import List
from typing import Dict

def get_inv_sim_bvalues(df: DataFrame, wrap_no_list : List, period : int, z_value : str) -> Dict:
    inv_sim_bvalues = []

    for wrap_no in wrap_no_list :
        inv_bvalue = {
            'wrapProductNo' : wrap_no,
            'key' : wrap_no + "_" + str(period-1) + "_" + z_value,
            'value' : df[df['key'] == wrap_no + "_" + str(period-1) + "_" + z_value]['value'].values[0]
        }

        inv_sim_bvalues.append(inv_bvalue)
    b_list = [b['value'] for b in inv_sim_bvalues]

    max_b = max(b_list)
    min_b = min(b_list)

    e = {}

    abs_rate = 0.5
    rel_rate = 1 - abs_rate
    max_inv_sim_bvalue = 100
    min_inv_sim_bvalue = 60
    # 절대평가/상대평가
    for x in inv_sim_bvalues :
        e[x['wrapProductNo']] = abs_rate*(max(round((x['value'] - max_b) * (10/0.1) + 100), 0)) + \
                                rel_rate*(round(((max_inv_sim_bvalue - min_inv_sim_bvalue) / (max_b - min_b)) * (x['value'] - min_b) + min_inv_sim_bvalue))

    return e