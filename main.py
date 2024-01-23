import pandas as pd
import numpy as np
from calculator import calculate_matching_score as CMS

import streamlit as st


wrap_list = ["WRAP00868", "WRAP00869", "WRAP00870", "WRAP00871", "WRAP00872", "WRAP00873", "WRAP00874", "WRAP00875"]

if __name__ == "__main__" :
    df_ib = pd.read_csv("./data/inv_sim_bvalues.csv")
    # print(CBS.get_inv_sim_bvalues(df_ib, wrap_list, 12, 0))
    df_rw = pd.read_csv("./data/risky_weight_scores.csv")
    # print()
    print(CMS.calculate_wrap(df_ib, df_rw, wrap_list, 12, 0, 'F01', 30))

    st.title("매칭점수 계산기(24.01.23)")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        period_select_box = st.selectbox("투자 기간(개월)", (12, 24, 36, 48))
        st.write('선택한 투자 기간:', period_select_box)
    with col2:
        z_value_select_box = st.selectbox("적립액/거치액 비율", (0, 0.0055, 0.007, 0.008))
        st.write('선택한 비율:', z_value_select_box)
    with col3:
        job_select_box = st.selectbox("직업", ('F01', 'F02', 'F03', 'F04'))
        st.write('선택한 직업:', job_select_box)
    with col4:
        age_select_box = st.selectbox("나이", (30, 40, 50, 60))
        st.write('선택한 나이:', age_select_box)


    st.write(CMS.calculate_wrap(df_ib, df_rw, wrap_list, period_select_box, z_value_select_box, job_select_box, age_select_box))
