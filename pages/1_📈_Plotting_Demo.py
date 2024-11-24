


import streamlit as st
import pandas as pd
import pydeck as pdk
from urllib.error import URLError
import sys

from millify import millify
from streamlit_extras.metric_cards import style_metric_cards

date_flag = "declaration_quarter"

import json
def load_cfg_json():
    with open("C:/Users/guswh/Desktop/data-analysis/workspace/study/ts_prj/config_ts.json", "r") as f: 
        cfg = json.load(f)
    return cfg
cfg = load_cfg_json()     
home = cfg['home']
st.logo(cfg['ts_prj']['logo'],  icon_image=cfg['ts_prj']['icon_logo'], size = "large")


title_name = "지역별 치매현황" 


st.set_page_config(page_title=title_name, page_icon="🔥", layout="wide")
#st.set_option('deprecation.showPyplotGlobalUse', False)
st.title(title_name)
#st.sidebar.header("riskmanagement_dashboard")




def mult_sel_def(data, col, check) :
    col_unique = data[col].unique()
    if check == "all" :
        mult_options = st.multiselect(
            'Select '+col+'(s):',
            options=col_unique,
            default=col_unique
        )
    elif check == "one" :
        mult_options = st.multiselect(
            'Select '+col+'(s):',
            options=col_unique,
            default=col_unique[0]
        )                
    else : 
        mult_options = st.multiselect(
            'Select '+col+'(s):',
            options=col_unique,
            default=check
        )                

    return mult_options


def convert_ymd_to_yQ(df, ymd_column):
    df[ymd_column] = pd.to_datetime(df[ymd_column])
    # y-m-d 형식의 컬럼에서 년과 분기를 추출합니다.
    df['Year'] = df[ymd_column].dt.year
    df['Quarter'] = df[ymd_column].dt.quarter

    # y-Q 형식의 새로운 컬럼을 만듭니다.
    df['declaration_quarter'] = df['Year'].astype(str) + '-Q' + df['Quarter'].astype(str)

    # 원래의 y-m-d 형식 컬럼을 제거합니다.
    df.drop(columns=['Year', 'Quarter'], inplace=True)
    return df


###################################################
#################### Data Read ####################
###################################################

#df0 = pd.read_csv(home + "data/보건복지부_시군구별 치매현황_20231231.csv")
df0 = pd.read_csv(home + "data/prep/df0.csv")
df0_summary = pd.read_csv(home + "data/prep/df0_summary.csv")

###################################################
###################################################
###################################################

tab0, tab1, tab2 = st.tabs(["tab0", "tab1" , "tab2"])

#연도 시도 시군구 성별   연령별 노인인구수
with tab0 :
    col1, col2, col3, col4 = st.columns(4)
    with col1 : 
        with st.expander("시도(펼치기/접기)") : 
            city_options=mult_sel_def(df0, '시도', "서울특별시")        
            filter_opt1 = df0[df0['시도'].isin(city_options)]
    with col2 : 
        with st.expander("시군구(펼치기/접기)") : 
            filter_opt2=mult_sel_def(filter_opt1, '시군구', "all")
    with col3 : 
        with st.expander("성별(펼치기/접기)") :           
            filter_opt3=mult_sel_def(filter_opt1, '성별', "one")
    with col4 : 
        with st.expander("연령별(펼치기/접기)") :              
            filter_opt4=mult_sel_def(filter_opt1, '연령별', "one")
        
        select_df0 = df0[df0['시도'].isin(city_options) &
                                df0['시군구'].isin(filter_opt2) &
                                df0['성별'].isin(filter_opt3) &
                                df0['연령별'].isin(filter_opt4)]
    
    
    dash_3 = st.container()
    dash_4 = st.container()

    # 치매환자유병률 최경도.환자 경도.환자 중등도.환자 중증.환자 경도인지장애.환자수
    with dash_3:
        # get kpi metrics
        total_ni = select_df0['노인인구수'].sum()
        total_ci = select_df0['치매환자수'].sum()
        total_cq = select_df0['최경도.환자'].sum()
        total_nw = select_df0['경도.환자'].sum()    
        total_de = select_df0['중등도.환자'].sum()
        total_ie = select_df0['중증.환자'].sum()
        total_te = select_df0['경도인지장애.환자수'].sum()

        total_ni = format(round(total_ni,0), ',')
        total_ci = format(round(total_ci,0), ',')        
        total_cq = format(round(total_cq,0), ',')
        total_nw = format(round(total_nw,0), ',')
        total_de = format(round(total_de,0), ',')
        total_ie = format(round(total_ie,0), ',')
        total_te = format(round(total_te,0), ',')

        col1, col2, col3, col4 = st.columns(4)
        # create column span
        # col1.metric(label="Chargeable Weight(ton)", value= total_cw, delta=-0.5,delta_color = "normal")
        col1.metric(label="노인인구수", value= total_ni)
        col2.metric(label="치매환자수", value= total_ci)
        col3.metric(label="최경도.환자", value= total_cq)
        col4.metric(label="경도.환자", value= total_nw)

        
        # this is used to style the metric card
        style_metric_cards(border_left_color="#DBF227", background_color = "@494a3e")  # color="red" 추가
    with dash_4 : 
        col5, col6, col7 = st.columns(3)
        col5.metric(label="중등도.환자", value= total_de)
        col6.metric(label="중증.환자", value= total_ie)
        col7.metric(label="경도인지장애.환자수", value= total_te)
        # this is used to style the metric card
        style_metric_cards(border_left_color="#DBF227", background_color = "@494a3e")  # color="red" 추가
    
    
    st.dataframe(select_df0, height = 400, hide_index = True)    



    select_df0_summary = df0_summary[df0_summary['시도'].isin(city_options) &
                            df0_summary['시군구'].isin(filter_opt2) &
                            df0_summary['성별'].isin(filter_opt3) &
                            df0_summary['연령별'].isin(filter_opt4)]


    st.dataframe(
        select_df0_summary[['시도','시군구','성별','연령별','치매환자유병률', '경도인지장애.환자유병률', '치매환자수']],
        column_config={
            "name": "App name",
            "stars": st.column_config.NumberColumn(
                "Github Stars",
                help="Number of stars on GitHub",
                format="%d ⭐",
            ),
            "치매환자유병률": st.column_config.LineChartColumn(
                "치매환자유병률", y_min=0, y_max=1,
            ),        
            "경도인지장애.환자유병률": st.column_config.LineChartColumn(
                "경도인지장애.환자유병률", y_min=0, y_max=10,
            ),        
            "치매환자수": st.column_config.LineChartColumn(
                "치매환자수", y_min=0, y_max=150,
            ),        

            # "노인인구수": st.column_config.LineChartColumn(
            #     "노인인구수", y_min=0, y_max=5000
            # ),
            # "치매환자수": st.column_config.LineChartColumn(
            #     "치매환자수", y_min=0, y_max=5000
            # ),
            # "최경도.환자": st.column_config.LineChartColumn(
            #     "최경도.환자", y_min=0, y_max=5000
            # ),
            # "경도.환자": st.column_config.LineChartColumn(
            #     "경도.환자", y_min=0, y_max=5000
            # ),
            # "중등도.환자": st.column_config.LineChartColumn(
            #     "중등도.환자", y_min=0, y_max=5000
            # ),
            # "중증.환자": st.column_config.LineChartColumn(
            #     "중증.환자", y_min=0, y_max=5000
            # ),
            # "경도인지장애.환자수": st.column_config.LineChartColumn(
            #     "경도인지장애.환자수", y_min=0, y_max=1,
            # ),        

            
        },
        hide_index=True,
    )

with tab1 : 
    st.write("hello")

    
    
with tab2 : 
    st.write("hello")    