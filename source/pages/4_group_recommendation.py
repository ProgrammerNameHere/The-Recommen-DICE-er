
# imports
import pandas as pd
import streamlit as st

from prediction import recommend

st.title('Group Recommendation Page under Construction')


# # Check if the DataFrame exists in session state
# if "ratings_df" in st.session_state and not st.session_state["ratings_df"].empty:
#     st.write("All Collected Ratings:")
#     st.dataframe(st.session_state["ratings_df"])
# else:
#     st.warning("No ratings found. Please add ratings.")


# Check if the DataFrame exists in session state and is not empty
if "ratings_df" in st.session_state and not st.session_state["ratings_df"].empty:
    ratings_df = st.session_state["ratings_df"]
    st.write("All Collected Ratings:")
    st.dataframe(ratings_df)

    # Initiate dict for saving individual user recommendations  
    user_recommendations = {}

    if st.button("Get Group Recommendations"):
        
        # Iterate through ratings dataframe and create recommendations for each user
        for username, group in st.session_state["ratings_df"].groupby("username"):
            
            rated_boardgames = group["boardgame"].unique().tolist()
            game_ids, game_names, query_features = recommend(rated_boardgames)    
            user_recommendations[username] = game_names
            
        # # Display the recommendations for each user
        # for user, recs in user_recommendations.items():
        #     st.write(f"User {user} recommendations: {recs}")
            
        # Create a list that includes all recommended boardgames 
        pooled_games_list = [item for sublist in user_recommendations.values() for item in sublist]
        # st.write(pooled_games_list)
        
        # Create group recommendation from pooled indivdual recommendations
        game_ids, game_names, query_features = recommend(pooled_games_list)    
        
        ranks = list(range(1, len(game_names) + 1))
        recommendations_df = pd.DataFrame({
                    "Rank": ranks,
                    "Game Name": game_names,
                    "ID": game_ids
                }) 
        
        st.markdown(recommendations_df.to_html(index=False), unsafe_allow_html=True)

    st.session_state["ratings_df"].to_csv('example_user_ratings.csv')
    
else:
    st.warning("No User data found. Please add ratings.")