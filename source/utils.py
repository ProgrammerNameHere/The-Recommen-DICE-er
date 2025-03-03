# add user functions here
import pandas as pd
import streamlit as st



def load_local_css(file_name: str):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# Function to select a list of games for rating
def ratelist(dataframe,ordered_by ='usersrated', games_to_rate = 10 ):
    # depending on the sorted column descending or ascending order is needed 
    if ordered_by in 'usersrated, average, bayesaverage':
        ascndng = False
    elif ordered_by in('rank'):
        ascndng = True
    # sort the full games data frame by the selected ordered_by column
    df_sorted = dataframe.sort_values(by=ordered_by, ascending=ascndng)
    # select the first x games (x= games_to_rate) 
    games_list = df_sorted['name'].head(games_to_rate).tolist()
    # a description text that can be printed
    select_desc = "Here are the top " + str(games_to_rate) + ' games by ' + ordered_by + ' for you:'
    # return a list of games and a string with a short description
    return games_list, select_desc


# Function to collect ratings
def collect_ratings(username, boardgames):
    ratings = []

    for game in boardgames:
        # Initialize session state only once per game
        if f"{game}_rating" not in st.session_state:
            st.session_state[f"{game}_rating"] = "I don't know"

        # Radio button for rating (session state key ensures persistence)
        rating = st.radio(
            f"Rate {game}:",
            options=["I don't know"] + [str(i) for i in range(11)],  # ['I don't know', '0', ..., '10']
            key=f"{game}_rating",
            horizontal=True
        )

        # Convert valid ratings to integer, keep "I don't know" as None
        ratings.append(None if rating == "I don't know" else int(rating))

    # Create a DataFrame
    return pd.DataFrame({'username': username, 'boardgame': boardgames, 'rating': ratings})