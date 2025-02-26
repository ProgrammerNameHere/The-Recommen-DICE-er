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




# Input for the first player
username = st.text_input("Enter your username:")

if username:
    # Create a search input for the game name
    search_text = st.text_input("Search for a board game:")

    # If there is input, filter the games in df_games
    if search_text:
        # Filter the games based on the search input (case insensitive)
        filtered_games = df_games[df_games['name'].str.contains(search_text, case=False, na=False)]

        # If there are matching results, show them in a selectbox
        if not filtered_games.empty:
           
            game_name = st.selectbox("Select a game", filtered_games['name'].tolist())
            st.write(f"You selected: {game_name}")
            boardgames=[game_name]  #pass variable game_name to list boardgames to avoid an error
            if st.button('Rate this game'): 
                #print(boardgames) #test print for content of parameter boardgames
                new_rating = collect_ratings(username,boardgames)
                print(new_rating) #test print what's the output of the function?
                st.write(new_rating)
                #st.session_state.ratings_df = pd.concat([st.session_state.ratings_df, new_rating], ignore_index=True)
        else:
            st.write("No games found matching that search.")
    else:
        st.write("Enter a board game name to search.")