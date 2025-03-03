# imports
import pandas as pd
import streamlit as st
import numpy as np
import tensorflow as tf
import tensorflow_recommenders as tfrs

from prediction import recommend
                  
 
st.title('Single Player Recommendation Page under Construction')

# Check if the DataFrame exists in session state
if "ratings_df" in st.session_state and not st.session_state["ratings_df"].empty:
    st.write("All Collected Ratings:")
    st.dataframe(st.session_state["ratings_df"])
else:
    st.warning("No ratings found. Please add ratings.")


    
def main():
    st.title("Game Recommendation System")
    st.write("Enter boardgame names manually or load your list of favorite games.")
    user_name = st.text_input("Enter your name:")


    game_input = st.text_input("Enter one or more games (separated by commas):")
    
    if st.button("Get Recommendations"):
        try:
            # Split the input string by commas and strip extra spaces
            game_list = [game.strip() for game in game_input.split(',') if game.strip()]
            
            # Pass the list of boardgames to the recommend function
            game_ids, game_names, query_features = recommend(game_list)
            
            ranks = list(range(1, len(game_names) + 1))
            recommendations_df = pd.DataFrame({
                "Rank": ranks,
                "Game Name": game_names,
                "ID": game_ids
            })      
        # Output the recommendations as a table.
            # st.table(recommendations_df)      
            st.markdown(recommendations_df.to_html(index=False), unsafe_allow_html=True)
     
        except Exception as e:
            st.error("An error occurred: " + str(e))
            
         # Button to load a saved list from session_state (set by another page)
         
    if st.button("Load Saved List"):
        try:
            # Check if the saved list exists in session_state
            # if "saved_list" in st.session_state and st.session_state["saved_list"]:
            #     saved_game_list = st.session_state["saved_list"]
                # st.write("Loaded saved list:", saved_game_list)
                # Use the saved list as input to get recommendations
            if "ratings_df" in st.session_state:
                ratings_df = st.session_state["ratings_df"]
                # Filter the dataframe for the provided user name
                user_ratings_df = ratings_df[ratings_df["username"] == user_name]
                # Extract unique boardgame names from the 'game' column (adjust column name if needed)
                saved_game_list = user_ratings_df["boardgame"].unique().tolist()
                st.write("Recommendation based on the following games: " + ", ".join(saved_game_list))

            # Use the saved list as input to get recommendations.
            game_ids, game_names, query_features = recommend(saved_game_list)    
            
            ranks = list(range(1, len(game_names) + 1))
            recommendations_df = pd.DataFrame({
                "Rank": ranks,
                "Game Name": game_names,
                "ID": game_ids
            })      
        #   Output the recommendations as a table.
            # st.table(recommendations_df)    
            st.markdown(recommendations_df.to_html(index=False), unsafe_allow_html=True)
    
        except Exception as e:
            st.error("An error occurred: " + str(e))     
    

if __name__ == "__main__":
    main()
