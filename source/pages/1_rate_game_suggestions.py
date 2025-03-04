'''
TODO: 
- create variable active_user for the entire page, only ask for username if active_user is not defined (session state?, dummyname?) 
 
'''

# imports
import streamlit as st
import pandas as pd

# import user functions
from utils import ratelist, collect_ratings


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

    ## Option to collect ratings from additional players
    #make_suggestion_button = st.button("Make a suggestion")
    #if make_suggestion_button:

    # Add a selectbox for number of games to rate 
    number_of_games = st.sidebar.selectbox(
        'How many games would you like to rate?',
        (5, 10, 20, 50)
    )

    # Add a selectbox for number of games to rate 
    sortvariable = st.sidebar.selectbox(
        'By wich order should we sort?',
        ('usersrated', 'rank' , 'average', 'bayesaverage')
    )
    ###########################
    # a bit dirty: just write the game list down here instead of using function game_list directly from function collect_ratings
    boardgames, desctext = ratelist(dataframe=df_games, ordered_by=sortvariable, games_to_rate=number_of_games)
    ###########################

    # Collect ratings for the first player
    new_data = collect_ratings(username, boardgames)

    
    # Button to submit the ratings
    if st.button("Submit Ratings for this player"):
        st.session_state.ratings_df = pd.concat([st.session_state.ratings_df, new_data], ignore_index=True)
        # Save ratings to CSV
        st.session_state.ratings_df.to_csv(ratings_file, index=False)
        st.write("Thank you for your ratings!")



# Display current ratings DataFrame (if any)
if not st.session_state.ratings_df.empty:
    with st.sidebar:
        st.write("All Ratings Collected:")
        st.write(st.session_state.ratings_df[['username', 'boardgame', 'rating']].sort_index(ascending=False))


