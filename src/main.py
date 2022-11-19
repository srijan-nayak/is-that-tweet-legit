import streamlit as st

from dotenv import load_dotenv
from os import environ as env

load_dotenv()

API_KEY = env["API_KEY"]
API_KEY_SECRET = env["API_KEY_SECRET"]
BEARER_TOKEN = env["BEARER_TOKEN"]

if __name__ == '__main__':
    st.write("# Is that Tweet legit?")
