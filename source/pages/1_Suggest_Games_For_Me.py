# imports
import streamlit as st
import pandas as pd

# import user functions
from utils import ratelist, collect_ratings

st.set_page_config(
    page_title="Get a suggestion",
    page_icon=":game_die:",
    layout="centered"
)

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
    number_of_games = st.slider(
        'How many games would you like to rate?',
        min_value= 5,
        max_value=50,
        step=5
    )
    
    sorting_dict = {
        'Best Rated Overall': 'rank',
        'Most Rated': 'usersrated',
        'Best Rated Abstract Games': 'abstracts_rank',
        'Best Rated Card Games': 'cgs_rank',
        'Best Rated Childrens Games': 'childrensgames_rank',
        'Best Rated Family Games': 'familygames_rank',
        'Best Rated Party Games': 'partygames_rank', 
        'Best Rated Strategy Games': 'strategygames_rank',
        'Best Rated Thematic Games': 'thematic_rank',
        'Best Rated War Games': 'wargames_rank',
    }
    # Add a selectbox for number of games to rate 
    sortvariable = st.selectbox(
        'By wich order should we sort?',
        options= sorting_dict.keys()
    )
    
    ###########################
    # a bit dirty: just write the game list down here instead of using function game_list directly from function collect_ratings
    boardgames, desctext = ratelist(dataframe=df_games, ordered_by=sorting_dict[sortvariable], games_to_rate=number_of_games)
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


