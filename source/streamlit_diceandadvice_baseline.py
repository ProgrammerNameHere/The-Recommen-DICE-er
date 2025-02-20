import streamlit as st
import pandas as pd

from baseline_model import get_recommendations, get_group_recommendations

# read full board games information file from csv
df_games = pd.read_csv('data/boardgames_ranks.csv')

st.title("Dice and Advice")
st.write("Welcome to Game (K)Nights' Dice and Advice! Our novel tool uses ai to recommend the best game for you and friends. Please enter your username and your favorite boardgame")

# Input for the first player
username = st.text_input("Enter your username:")

# Create a search input for the game name
search_text = st.text_input("Search for a board game:")
# If there is input, filter the games in df_games
if search_text:
    # Filter the games based on the search input (case insensitive)
    filtered_games = df_games[df_games['name'].str.contains(search_text, case=False, na=False)]

    # If there are matching results, show them in a selectbox
    if not filtered_games.empty:
        game = st.selectbox("Select a game", filtered_games['name'].tolist())
        st.write(f"You selected: {game}")
    else:
        st.write("No games found matching that search.")
else:
    st.write("Enter the board game name or a part of it and press Enter to open a selection list")


if st.button("Get recommendations"):
    recommendations = get_recommendations(game_title=game)
    #if recommendations:
    st.write('Hi ' + username + ', the Top 10 recommended boardgames based on your selection "'+ game +'" are:')
    st.write(recommendations[['name', 'description']])