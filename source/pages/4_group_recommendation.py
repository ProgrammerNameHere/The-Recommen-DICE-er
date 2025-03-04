
# imports
import pandas as pd
import streamlit as st
import matplotlib.cm as cm
import matplotlib.colors as mcolors

from prediction import recommend
from model_utils import gradient_style, styled_scrollable_table

st.set_page_config(
    page_title="Group Recommendation",
    page_icon=":game_die:",
    layout="centered"
)


st.title('Group Recommendation')


# # Check if the DataFrame exists in session state
# if "ratings_df" in st.session_state and not st.session_state["ratings_df"].empty:
#     st.write("All Collected Ratings:")
#     st.dataframe(st.session_state["ratings_df"])
# else:
#     st.warning("No ratings found. Please add ratings.")

df_for_player_numbers = pd.read_csv('data/game_details_raw.csv')

df_for_player_numbers = df_for_player_numbers[['game_id','name', 'minplayers', 'maxplayers']]

# Check if the DataFrame exists in session state and is not empty
if "ratings_df" in st.session_state and not st.session_state["ratings_df"].empty:
    ratings_df = st.session_state["ratings_df"]
    st.write("All Collected Ratings:")
    # st.markdown(ratings_df.drop('Unnamed: 0',axis=1).to_html(index=False), unsafe_allow_html=True)
        # Get the styled, scrollable table HTML
    table_html = styled_scrollable_table(ratings_df.drop('Unnamed: 0', axis=1), username_column="username", cmap_name="tab20c", max_height="400px")

# Render the table in Streamlit
    st.markdown(table_html, unsafe_allow_html=True)

    # Create a slider widget to select number of players for filtering recommendations
    player_number = st.slider("How many players?", min_value=1, max_value=8, value=4, step=1)
    
    # Initiate dict for saving individual user recommendations  
    user_recommendations = {}

    if st.button("Get Group Recommendations"):
        
        # Iterate through ratings dataframe and create recommendations for each user
        for username, group in st.session_state["ratings_df"].groupby("username"):
            
            rated_boardgames = group["boardgame"].unique().tolist()
            game_ids, game_names, query_features = recommend(rated_boardgames)    
            user_recommendations[username] = game_names
            
            
        # Create a list that includes all recommended boardgames 
        pooled_games_list = [item for sublist in user_recommendations.values() for item in sublist]
        # st.write(pooled_games_list)
        
        # Create group recommendation from pooled indivdual recommendations
        game_ids, game_names, query_features = recommend(pooled_games_list)    
        
        # filtered_df = df_for_player_numbers[df_for_player_numbers['game_id'].isin(game_ids)]
        filtered_recs_df = df_for_player_numbers[
                (df_for_player_numbers['game_id'].isin(game_ids)) &
                (df_for_player_numbers['name'].isin(game_names)) &
                (df_for_player_numbers['minplayers'] <= player_number) &
                (df_for_player_numbers['maxplayers'] >= player_number)
        ]

        ranks = list(range(1, len(filtered_recs_df) + 1))
        recommendations_df = pd.DataFrame({
            "Rank": ranks,
            "Game Name": filtered_recs_df.name,
            "ID": filtered_recs_df.game_id
        })
         
        recommendations_df = recommendations_df.reset_index(drop=True)

    #   Output the recommendations as a table.
        # st.table(recommendations_df) 
        styled_table = recommendations_df.head(10).style.apply(
        lambda row: gradient_style(row, len(recommendations_df)), axis=1).to_html(index=False)
        st.markdown(styled_table, unsafe_allow_html=True) 

    # st.session_state["ratings_df"].to_csv('example_user_ratings.csv')
    
else:
    st.warning("No User data found. Please add ratings.")