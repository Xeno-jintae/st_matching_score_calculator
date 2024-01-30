import pandas as pd
from pandas import DataFrame
import plotly.express as px


from calculator import calculate_matching_score as CMS

def make_rank(wrap_no, df1, df2, wrap_list, period, z_value, job, age) :
    df = CMS.calculate_wrap(df1, df2, wrap_list, period, z_value, job, age)
    return int(df[df['wrapProductNo'] == wrap_no]['rank'].values[0])

def change_job_list(df1, df2, wrap_list, period, z_value, age):
    dic = {'wrapProductNo' : wrap_list}
    for job_code in ['F01', 'F02', 'F03', 'F04', 'F05', 'F06', 'F07', 'F08', 'F09', 'F10', 'F11', 'F12', 'F13']:
        dic[job_code] = []
        for wrap in wrap_list :
            rank = make_rank(wrap, df1, df2, wrap_list, period, z_value, job_code, age)
            dic[job_code].append(rank)
    df = pd.DataFrame(dic)
    list1 = []

    for i in range(df.shape[0]):
        unique_value_count = len(df.iloc[i,1:].unique())
        list1.append(unique_value_count)
    df['unique_value_count'] = list1

    return df

def make_heatmap_for_unique_value(wrapPrductNo, z_value, df1, df2, wrap_list):
    heat_dic = {}
    for age in [*range(25,40)]:
        heat_dic[age] = []
        for period in [*range(12, 36, 6)]:
            df = change_job_list(df1, df2, wrap_list, period, z_value, age)
            unique_value = df[df['wrapProductNo'] == wrapPrductNo]['unique_value_count'].values[0]
            heat_dic[age].append(unique_value)
    df = pd.DataFrame(heat_dic)
    df.index = [str(x) + '개월' for x in range(12, 36, 6)]
    df.columns = [str(x) +'세' for x in range(25,40)]

    df.to_csv(f"./data/unique_value_count/unique_{wrapPrductNo}_{z_value}_{age}_{period}.csv", encoding='utf-8-sig')

    fig = px.imshow(df, text_auto = True)

    return fig

def make_heatmap_csv(wrapProductNo, z_value=0):
    df = pd.read_csv(f"./data/unique_value/unique_value_{wrapProductNo}_{z_value}.csv", index_col=0)
    fig = px.imshow(df, text_auto = True, width=1000, height=1000, aspect='auto')

    return fig