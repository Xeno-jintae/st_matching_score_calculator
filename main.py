import pandas as pd
import numpy as np
from calculator import calculate_matching_score as CMS
from util import common
import streamlit as st

from case_calculator import job_case_calculator


wrap_list = ["WRAP00868", "WRAP00869", "WRAP00870", "WRAP00871", "WRAP00872", "WRAP00873", "WRAP00874", "WRAP00875"]

if __name__ == "__main__" :
    wrap_name = pd.read_csv("./data/wrap_name.csv")
    print(wrap_name)
    df_ib = pd.read_csv("./data/inv_sim_bvalues.csv")
    df_rw = pd.read_csv("./data/risky_weight_scores.csv")
    # print(CMS.calculate_wrap(df_ib, df_rw, wrap_list, 12, 0, 'F01', 30))
    st.set_page_config(layout="wide")
    st.title("매칭점수 계산기(24.01.23)")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        period_select_box = st.selectbox("투자 기간(개월)", ([*range(12, 361, 6)]))
        st.write('선택한 투자 기간:', str(period_select_box) + '개월')
    with col2:
        z_value_select_box = st.selectbox("적립액/거치액 비율", (common.Z76))
        st.write('선택한 비율:', z_value_select_box)
    with col3:
        job_select_box = st.selectbox("직업", (sorted(list(set([x.split("_")[1] for x in df_rw['key']])))))
        st.write('선택한 직업:', job_select_box)
    with col4:
        age_select_box = st.selectbox("나이", ([*range(25, 64)]))
        st.write('선택한 나이:', str(age_select_box) + '세')


    df1 = pd.merge(CMS.calculate_wrap(df_ib, df_rw, wrap_list, period_select_box, z_value_select_box, job_select_box, age_select_box), wrap_name, left_on='wrapProductNo', right_on='wrapProductNo')
    df1 = df1[['wrapProductNo', 'wrapProductName', 'matchingScore', 'rank']]
    st.write(df1)

    st.subheader('직업에 대한 민감도', divider='rainbow')
    col5, col6 = st.columns([0.3,1.2])
    with col5:
        period_sb = st.selectbox("1. 투자 기간(개월)", ([*range(12, 361, 6)]))
        z_value_sb = st.selectbox("1. 적립액/거치액 비율", (common.Z76))
        age_sb = st.selectbox("1. 나이", ([*range(25, 64)]))
    with col6:
        df_account = job_case_calculator.change_job(df_ib, df_rw, wrap_list, period_sb, z_value_sb, age_sb)
        st.write(job_case_calculator.make_columns(df_account))
