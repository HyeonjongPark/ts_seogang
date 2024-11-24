import streamlit as st

import yaml
import streamlit as st
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
from streamlit_authenticator.utilities.exceptions import (CredentialsError,
                                                          ForgotError,
                                                          LoginError,
                                                          RegisterError,
                                                          ResetError,
                                                          UpdateError) 


import traceback

import streamlit as st
from st_social_media_links import SocialMediaIcons
from streamlit.components.v1 import html as st_html

#import st_login_form




import json
def load_cfg_json():
    with open("C:/Users/guswh/Desktop/data-analysis/workspace/study/ts_prj/config_ts.json", "r") as f: 
        cfg = json.load(f)
    return cfg
cfg = load_cfg_json()     
st.logo(cfg['ts_prj']['logo'],  icon_image=cfg['ts_prj']['icon_logo'], size = "large")


VERSION = '1.0.0'

title_name = "seogang_ts"

st.set_page_config(
    page_title=title_name,
    page_icon="🔐",
    menu_items={
        "About": f"Streamlit Login Form 🔐 v{VERSION}  "
        f"\nApp contact: [Siddhant Sadangi](mailto:siddhant.sadangi@gmail.com)",
        "Report a Bug": "https://github.com/SiddhantSadangi/st-login-form/issues/new",
        "Get help": None,
    },
)

st.markdown("""
    <style>
        section[data-testid="stSidebar"][aria-expanded="true"]{
            display: none;
        }
    </style>
    """, unsafe_allow_html=True)






# Loading config file
with open('./config.yaml', 'r', encoding='utf-8') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Creating the authenticator object
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    #config['pre-authorized']
)

st.success(
    title_name + "에 오신 것을 환영합니다. ", #"[Star the repo](https://github.com/SiddhantSadangi/st_login_form) to show your :heart:",
    icon="⭐",
)


# Creating a login widget
try:
    authenticator.login()
except LoginError as e:
    st.error(e)

if st.session_state["authentication_status"]:
    # side panel 숨김 해제
    st.markdown("""
        <style>
            section[data-testid="stSidebar"][aria-expanded="true"]{
                display: block;
            }
        </style>
        """, unsafe_allow_html=True)    

    st.write(f'Welcome *{st.session_state["name"]}*')

    #st.write("# 👋 Welcome to Procurement Negotiation Platform! 👋")
    st.title("🔐 Welcome to " + title_name)

    st.sidebar.success("Select Menu.")

    st.markdown(
        """
        **👈 좌측 사이드 바에 있는 버튼 클릭시 페이지 이동합니다.
        ### side tab1
        - xx
        ### side tab2
        - xx
        ### 참고 URL
        - reference
        
    """
    )
    #authenticator.logout()  

    
elif st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your username and password')


# Saving config file
with open('./config.yaml', 'w', encoding='utf-8') as file:
    yaml.dump(config, file, default_flow_style=False)



try:
    # ---------- SIDEBAR ----------
    with open("assets/sidebar.html", "r", encoding="UTF-8") as sidebar_file:
        sidebar_html = sidebar_file.read().replace("{VERSION}", VERSION)

    # with st.sidebar:
    #     st_html(sidebar_html, height=243)

    #     st.html(
    #         """
    #         <div style="text-align:center; font-size:14px; color:lightgrey">
    #             <hr style="margin-bottom: 6%; margin-top: 0%;">
    #             CDO (hyeonjong.park@lge.com)
    #         </div>"""
    #     )
    #     authenticator.logout()


except Exception as e:
    st.error(
        f"""The app has encountered an error:\n
`{e}`\n
Please create an issue [here](https://github.com/SiddhantSadangi/st_login_form/issues/new)
with the below traceback""",
        icon="🥺",
    )
    st.code(traceback.format_exc())












# Set the background image
background_image = """
<style>
[data-testid="stAppViewContainer"] > .main {
    background-image: url("https://img.freepik.com/free-vector/abstract-realistic-technology-particle-background_23-2148420656.jpg?t=st=1721348980~exp=1721352580~hmac=ba77b2040528171813b223c4bb51741e55c11bc67e43bbdd68d34bc6863b02bb&w=1380");
    background-size: 100vw 100vh;  # This sets the size to cover 100% of the viewport width and height
    background-position: center;  
    background-repeat: no-repeat;
}
</style>
"""
#st.markdown(background_image, unsafe_allow_html=True)
