# imports
import pandas as pd
import streamlit as st

st.title('Single Player Recommendation Page under Construction')

# Check if the DataFrame exists in session state
if "ratings_df" in st.session_state and not st.session_state["ratings_df"].empty:
    st.write("All Collected Ratings:")
    st.dataframe(st.session_state["ratings_df"])
else:
    st.warning("No ratings found. Please add ratings.")
