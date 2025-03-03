# imports
import pandas as pd
import streamlit as st
import numpy as np
import tensorflow as tf
import tensorflow_recommenders as tfrs

from model_utils import get_recommendation
                  

st.title('Single Player Recommendation Page under Construction')

# Check if the DataFrame exists in session state
if "ratings_df" in st.session_state and not st.session_state["ratings_df"].empty:
    st.write("All Collected Ratings:")
    st.dataframe(st.session_state["ratings_df"])
else:
    st.warning("No ratings found. Please add ratings.")



input = st.text_input("Enter your favorite boardgame:")

if input:
    st.write(f"You entered: {input}")     

    game_ids, game_names, query_features = get_recommendation('input')

    st.write(f'You should play: {game_names}')