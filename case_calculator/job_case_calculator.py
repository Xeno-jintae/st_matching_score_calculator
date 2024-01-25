from pandas import DataFrame
from typing import Dict
from typing import List
from typing import Tuple

import pandas as pd

from calculator import calculate_matching_score as CMS

def make_rank_score(wrap_no : str, df1 : DataFrame, df2 : DataFrame, wrap_list : List, period : int, z_value : str, job : str, age: int) -> Tuple :
    df = CMS.calculate_wrap(df1, df2, wrap_list, period, z_value, job, age)
    return int(df[df['wrapProductNo']==wrap_no]['rank'].values[0]), round(max(list(df['matchingScore'])),3), round(min(list(df['matchingScore'])),3)

def change_job(df1 : DataFrame, df2 : DataFrame, wrap_list : List, period : int, z_value : str, age: int) -> DataFrame:
    dic = {'wrapProduct' : wrap_list + ['최고 점수', '최저 점수']}
    for job_code in ['F01', 'F02', 'F03', 'F04', 'F05', 'F06', 'F07', 'F08', 'F09', 'F10', 'F11', 'F12', 'F13']:
        dic[job_code] = []
        for idx, wrap in enumerate(wrap_list):
            rank, max_score, min_score = make_rank_score(wrap, df1, df2, wrap_list, period, z_value, job_code, age)

            dic[job_code].append(rank)

            if idx==7:
                dic[job_code].append(max_score)
                dic[job_code].append(min_score)
    return pd.DataFrame(dic)

def _make_list_length(a: List) -> List:
    a2 = a + ['-', '-']
    return a2

def _make_list_sum(a: List) -> List:
    a2 = a + [sum(a), '-']
    return a2

def make_columns(df : DataFrame) :
    list1 = []
    list2 = []
    list3 = []
    list4 = []
    for i in range(df.shape[0]-2) :
        unique_value_count = len(df.iloc[i, 1:].unique())
        mode_value_count = sum(df.iloc[i, 1:] == df.iloc[i, 1:].mode().values[0])
        mode_value_percent = mode_value_count/13
        mode_value_percent_square = mode_value_percent**2

        list1.append(unique_value_count)
        list2.append(mode_value_count)
        list3.append(mode_value_percent)
        list4.append(mode_value_percent_square)

    df['unique_value_count'] = _make_list_sum(list1)
    df['mode_value_count'] = _make_list_sum(list2)
    df['mode_value_percent'] = _make_list_length([round(x,2) for x in list3])
    df['mode_value_percent_square'] = _make_list_sum(list4)

    return df

