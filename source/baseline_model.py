import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

# read data from csv files
df_names = pd.read_csv('data/boardgames_ranks.csv').query('rank > 0')
df_description = pd.read_csv('data/game_details.csv')

# merge game basics and details
df = pd.merge(df_names, df_description, left_on='id', right_on='game_id')
df['description'] = df['description'].fillna('')


# Create a TfidfVectorizer and Remove stopwords
tfidf = TfidfVectorizer(stop_words='english')
# Fit and transform the data to a tfidf matrix
tfidf_matrix = tfidf.fit_transform(df['description'])
# Print the shape of the tfidf_matrix
tfidf_matrix.shape
# Compute the cosine similarity between each movie description
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
indices = pd.Series(df.index, index=df['name']).drop_duplicates()


# define basic function for item-item similarity based recommendation
def _get_recommendations(name, cosine_sim=cosine_sim, num_recommend = 10):
    idx = indices[name]
# Get the pairwsie similarity scores of all games with that game
    sim_scores = list(enumerate(cosine_sim[idx]))
# Sort the games based on the similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
# Get the scores of the 10 most similar games
    top_similar = sim_scores[1:num_recommend+1]
# Get the game indices
    game_indices = [i[0] for i in top_similar]
# Return the top 10 most similar games
    return df['name'].iloc[game_indices]

# test the function
# game = 'Ticket to Ride'
# test_recommendations = _get_recommendations(game, num_recommend = 50)
# type(test_recommendations)

# define function for single player recommendation
def get_recommendations(game_title, number_of_recommendations = 10):
    games = _get_recommendations(game_title, num_recommend= number_of_recommendations)
    return df[df['name'].isin(games.to_list())].drop(columns=['id_y'])

# test the function
#game = input('Please enter a game name:') 
#print(get_recommendations(game, number_of_recommendations = 10))

# define function for group recommendation
def get_group_recommendations(game_titles, number_of_recommendations = 10):
    for game_title in game_titles:
        recommended_games = _get_recommendations(game_title, num_recommend= number_of_recommendations)
    return df[df['name'].isin(recommended_games.to_list())].drop(columns=['id_y'])