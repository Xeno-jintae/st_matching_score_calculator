from pandas import DataFrame
from typing import List
from typing import Dict

def get_risky_weight_score(df:DataFrame, wrap_no_list: List, job_code : str, age : int) -> Dict:
    risky_weight_scores = []

    for wrap_no in wrap_no_list :
        risky_weight_score = {
            'wrapProductNo' : wrap_no,
            'key' : wrap_no + "_" + job_code + "_" + str(age),
            'value' : df[df['key'].str.contains(wrap_no + "_" + job_code + "_" + str(age))]['value'].values[0]
        }
        risky_weight_scores.append(risky_weight_score)

    e = {}
    for x in risky_weight_scores :
        e[x['wrapProductNo']] = x['value']

    return e