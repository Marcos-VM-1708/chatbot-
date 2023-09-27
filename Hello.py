import streamlit as st
from streamlit.logger import get_logger

# ----------------------------------------------------------------------------------

LOGGER = get_logger(__name__)


# ----------------------------------------------------------------------------------
def run()
  st.set_page_config(page_title="Chat Bernhoeft - Gestão de Terceirizados", layout="wide", initial_sidebar_state="collapsed")
  st.title("Chat Bernhoeft - Gestão de Terceirizados")

  hide_streamlit_style = """
              <style>
              #MainMenu {visibility: hidden;}
              header {visibility: hidden;}
              [data-testid="collapsedControl"] {visibility: hidden;}
              footer {visibility: hidden;}
              </style>
              """
  st.markdown(hide_streamlit_style, unsafe_allow_html=True)

if __name__ == "__main__":
    run()
