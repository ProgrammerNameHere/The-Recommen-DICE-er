# add user functions here
import pandas as pd
import streamlit as st

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


# Function to collect ratings for one player
def collect_ratings(username, boardgames):
    ratings = []
    for game in boardgames:
        # Ask if the user knows the game
        know_game = st.radio(f"Please Rate {game}:", ["I don't know", '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10'], key=f"{game}_know", horizontal = True)
        
        if know_game == "I don't know":
            # Ask for a rating if they know the game
            ratings.append(None)
        else:
            # Ask for a rating if they know the game
            rating = know_game
            ratings.append(rating)

    # Create a new DataFrame for this user's ratings
    new_data = pd.DataFrame({
        'username': [username] * len(boardgames),
        'boardgame': boardgames,
        'rating': ratings
    })

    return new_data
    