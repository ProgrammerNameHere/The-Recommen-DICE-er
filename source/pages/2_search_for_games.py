'''
TODO: 
- create variable active_user for the entire page, only ask for username if active_user is not defined (session state?, dummyname?) 

ERROR: !!! function collect_ratings returns the value before the rating (=None) to the ratings dataframe but not the rating 
'''
# imports
import streamlit as st
import pandas as pd

# import user functions
from utils import collect_ratings

#from utils import ratelist(), collect_ratings()
# read full board games information file from csv
df_games = pd.read_csv('data/game_details_cleaned.csv')

# File path for storing ratings data
ratings_file = "data/ratings.csv"

# Initialize an empty DataFrame in session state if not already created
if 'ratings_df' not in st.session_state:
    # Try to load existing ratings from the CSV if it exists
    try:
        st.session_state.ratings_df = pd.read_csv(ratings_file)
    except FileNotFoundError:
        st.session_state.ratings_df = pd.DataFrame(columns=['username', 'boardgame', 'rating'])



username = st.text_input("Enter your username:")

if username:
    
    # Convert column to list for autocomplete
    autocomplete_list = [''] + df_games['name'].tolist()

    # Using a selectbox for autocomplete
    selected_name = st.selectbox("Choose a name", options=autocomplete_list)

    # Display the selected name
    st.write(f"You selected: {selected_name}")

# If there are matching results, show them in a selectbox
    if selected_name:
        
        boardgames=[selected_name]  #pass variable game_name to list boardgames to avoid an error

        # Ensure session state stores ratings DataFrame
        if "ratings_df" not in st.session_state:
            st.session_state["ratings_df"] = pd.DataFrame(columns=["username", "boardgame", "rating"])

        # Collect ratings
        ratings_df = collect_ratings(username, boardgames)

        # Submit button
        if st.button("Submit Ratings"):
            st.session_state["ratings_df"] = pd.concat([st.session_state["ratings_df"], ratings_df], ignore_index=True)
            st.success("Ratings submitted!")

        # Display stored ratings
        st.write("Collected Ratings:")
        st.dataframe(st.session_state["ratings_df"])
