import streamlit as st

import json
def load_cfg_json():
    with open("C:/Users/guswh/Desktop/data-analysis/workspace/study/ts_prj/config_ts.json", "r") as f: 
        cfg = json.load(f)
    return cfg
cfg = load_cfg_json()     
home = cfg['home']
st.logo(cfg['ts_prj']['logo'],  icon_image=cfg['ts_prj']['icon_logo'], size = "large")

title_name = "Eda"
st.set_page_config(page_title=title_name, page_icon="🔥", layout="wide")


st.html(home + "report.html")
