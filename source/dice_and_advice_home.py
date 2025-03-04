# imports
# from setup import *
import streamlit as st

st.set_page_config(
    page_title="Dice and Advice",
    page_icon=":game_die:",
    layout="centered"
)

from PIL import Image



# Welcome Page
st.title("Welcome to Dice and Advice")
st.write("---")
st.write("Presented by Game(K)Nights")

logo = Image.open("source/logo.png")
st.sidebar.image(logo, width=300)

st.header("Rate your favorite Games!")

st.header("Get a recommendation tailored just for you!")
    
st.header("or")
st.header("Get a recommendation for the whole group!")