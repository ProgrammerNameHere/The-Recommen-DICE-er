# imports
import streamlit as st

st.set_page_config(
    page_title="Individual Recommendation",
    page_icon=":game_die:",
    layout="centered"
)

import pandas as pd
import numpy as np

import tensorflow as tf
import tensorflow_recommenders as tfrs

from prediction import recommend
from model_utils import gradient_style, styled_scrollable_table
                            
                            
st.title('Get Individual Recommendation based on your Ratings')

# Check if the DataFrame exists in session state
if "ratings_df" in st.session_state and not st.session_state["ratings_df"].empty:
    st.write("Available Users:")
    ratings_df = st.session_state["ratings_df"]
    
    
    # Get the styled, scrollable table HTML
    table_html = styled_scrollable_table(ratings_df.drop('Unnamed: 0', axis=1), username_column="username", cmap_name="tab20c", max_height="400px")

# Render the table in Streamlit
    st.markdown(table_html, unsafe_allow_html=True)

else:
    st.warning("No ratings found. Please add ratings.")


df_for_player_numbers = pd.read_csv('data/game_details_raw.csv')
df_for_player_numbers = df_for_player_numbers[['game_id','name', 'minplayers', 'maxplayers', 'description']]

ratings_df = st.session_state["ratings_df"]

usernames = ratings_df['username'].unique()
selected_user = st.selectbox("Select a user", usernames)
st.write("You selected:", selected_user)

# Create a slider widget to select number of players for filtering recommendations
player_number = st.slider("How many players?", min_value=1, max_value=8, value=4, step=1, key='num_player_1')
    
if st.button("Get Recommendations", key="recs_1"):
    try:
        # Check if the saved list exists in session_state
        # if "saved_list" in st.session_state and st.session_state["saved_list"]:
        #     saved_game_list = st.session_state["saved_list"]
            # st.write("Loaded saved list:", saved_game_list)
            # Use the saved list as input to get recommendations
        if "ratings_df" in st.session_state:
            ratings_df = st.session_state["ratings_df"]
            # Filter the dataframe for the provided user name
            user_ratings_df = ratings_df[ratings_df["username"] == selected_user]
            # Filter out negative ratings (below 5)
            user_ratings_df = user_ratings_df[user_ratings_df["rating"] >= 5]
            # Extract unique boardgame names from the 'game' column (adjust column name if needed)
            saved_game_list = user_ratings_df["boardgame"].unique().tolist()
            st.write("Recommendation based on the following games: " + ", ".join(saved_game_list))

        # Use the saved list as input to get recommendations.
        game_ids, game_names, query_features = recommend(saved_game_list)   
        
    
        # filtered_df = df_for_player_numbers[df_for_player_numbers['game_id'].isin(game_ids)]
        filtered_recs_df = df_for_player_numbers[
                (df_for_player_numbers['game_id'].isin(game_ids)) &
                (df_for_player_numbers['name'].isin(game_names)) &
                (df_for_player_numbers['minplayers'] <= player_number) &
                (df_for_player_numbers['maxplayers'] >= player_number)
        ]
                
        bgg_url = "https://www.boardgamegeek.com/boardgame/"
        game_name_dict = dict(zip(filtered_recs_df.game_id, filtered_recs_df.name))
        ranks = list(range(1, len(filtered_recs_df) + 1))
        recommendations_df = pd.DataFrame({
            "Rank": ranks,
            "Game Name": filtered_recs_df.game_id.map(
                lambda x: f'<a href="{bgg_url+str(x)}"> {game_name_dict.get(x, "Unknown")}</a>'),
            "ID": filtered_recs_df.game_id,

        })
        
        
        recommendations_df = recommendations_df.reset_index(drop=True)


        
        # Output the recommendations as a table.
        # st.table(recommendations_df) 
        styled_table = recommendations_df.head(10).style.apply(
        lambda row: gradient_style(row, len(recommendations_df)), axis=1).to_html(index=False)
        

        st.markdown(styled_table, unsafe_allow_html=True)

    except Exception as e:
        st.error("An error occurred: " + str(e))     



        
st.title('Get Recommendation based on selected Games')

game_input = st.text_input("Enter one or more games (separated by commas):")

# Create a slider widget to select number of players for filtering recommendations
player_number = st.slider("How many players?", min_value=1, max_value=8, value=4, step=1, key='num_player_2')

if st.button("Get Recommendations", key="recs_2"):
    try:
        # Split the input string by commas and strip extra spaces
        game_list = [game.strip() for game in game_input.split(',') if game.strip()]
        
        # Pass the list of boardgames to the recommend function
        game_ids, game_names, query_features = recommend(game_list)
        
        # filtered_df = df_for_player_numbers[df_for_player_numbers['game_id'].isin(game_ids)]
        filtered_recs_df = df_for_player_numbers[
                (df_for_player_numbers['game_id'].isin(game_ids)) &
                (df_for_player_numbers['name'].isin(game_names)) &
                (df_for_player_numbers['minplayers'] <= player_number) &
                (df_for_player_numbers['maxplayers'] >= player_number)
        ]

        bgg_url = "https://www.boardgamegeek.com/boardgame/"
        game_name_dict = dict(zip(filtered_recs_df.game_id, filtered_recs_df.name))
        ranks = list(range(1, len(filtered_recs_df) + 1))
        recommendations_df = pd.DataFrame({
            "Rank": ranks,
            "Game Name": filtered_recs_df.game_id.map(
                lambda x: f'<a href="{bgg_url+str(x)}"> {game_name_dict.get(x, "Unknown")}</a>'),
            "ID": filtered_recs_df.game_id,

        })
        recommendations_df = recommendations_df.reset_index(drop=True)
        
        styled_table = recommendations_df.head(10).style.apply(
        lambda row: gradient_style(row, len(recommendations_df)), axis=1).to_html(index=False)
        
        st.markdown(styled_table, unsafe_allow_html=True)

    
    except Exception as e:
        st.error("An error occurred: " + str(e))
        
        # Button to load a saved list from session_state (set by another page)