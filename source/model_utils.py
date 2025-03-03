import pandas as pd
import numpy as np
import tensorflow as tf
import tensorflow_recommenders as tfrs
from sklearn.model_selection import train_test_split

RSEED = 42

def load_data(filepath):
    df = pd.read_csv(filepath)
    
    return df


def preprocess_data(df_complete):
    
    # Extract features
    df_features = df_complete.drop(['name', 'yearpublished','rank', 'bayesaverage', 'average',
       'usersrated', 'is_expansion', 'abstracts_rank', 'cgs_rank',
       'childrensgames_rank','familygames_rank', 'partygames_rank', 'strategygames_rank',
       'thematic_rank', 'wargames_rank', 'averageweight', 'boardgameartists',
       'boardgamecategories', 'boardgamedesigners', 'boardgamefamilies','boardgamemechanics', 'community_best_with',
       'community_recommended_with', 'description', 'game_id', 'maxplayers',
       'maxplaytime', 'median', 'minage', 'minplayers','minplaytime', 'numcomments', 'numweights', 'owned','stddev', 'trading', 'wanting', 'wishing',], axis=1)
    
    # Create game id dataset (important for indexing later)
    df_game_ids = df_complete['game_id']
    
    # List of features for model building
    feature_list = df_features.columns.to_list()
    
    return(df_features, df_game_ids, feature_list)

# Create candidate dictionary with features and game_id keys 
def create_candidate_dict(df_features, df_ids):
    candidate_data_dict = {
        "features": [],
        "game_id": []
    }

    for index, feature_row in df_features.iterrows():
        candidate_data_dict["features"].append(feature_row.tolist())  
        candidate_data_dict["game_id"].append(df_ids.iloc[index])

    return candidate_data_dict


def create_candidate_dataset(candidate_data_dict, batch_size=32):

    # Convert the list into a tensorflow dataset
    candidate_dataset = tf.data.Dataset.from_tensor_slices(candidate_data_dict)

    # Batch data for optimization
    candidate_dataset = candidate_dataset.batch(batch_size)
    
    return candidate_dataset

# Function for creating train, validation and test tensorflow datasets

def create_tf_datasets(df_features, test_size=0.2, random_state=RSEED, batch_size=32):

    # Split feature dataset into train, validation, and test sets
    train_data, test_data = train_test_split(df_features, test_size=0.2, random_state=RSEED)
    train_data, val_data = train_test_split(train_data, test_size=test_size*0.5, random_state=RSEED)

    def df_to_dataset(dataframe, shuffle=True, batch_size=batch_size):
        dataframe = dataframe.copy()
        ds = tf.data.Dataset.from_tensor_slices({"features": dataframe.to_numpy()})
        if shuffle:
            ds = ds.shuffle(buffer_size=len(dataframe))
        ds = ds.batch(batch_size)
        return ds

    train_ds = df_to_dataset(train_data, batch_size=batch_size)
    val_ds = df_to_dataset(val_data, shuffle=False, batch_size=batch_size)
    test_ds = df_to_dataset(test_data, shuffle=False, batch_size=batch_size)
    
    return train_ds, val_ds, test_ds


def create_retrieval_index(model, candidate_dataset):

    index = tfrs.layers.factorized_top_k.BruteForce(model.boardgame_model)
    index.index_from_dataset(
        candidate_dataset.map(lambda x: (x["game_id"], model.boardgame_model(x["features"])))
    )
    return index


def create_input_df(df_complete, feature_list):

    feature_list.append('name')
    df_input = df_complete[feature_list]
    
    return df_input


def get_recommendation(user_input, df_complete, df_input, index):

    user_input = user_input

    user_input_game_id = df_complete.loc[df_complete['name'] == user_input, 'game_id'].values

    query_features = np.array(df_input[df_input['name'] == user_input].iloc[:, 0:-1].values.tolist())
    
    scores, recommended_game_ids = index(query_features, k=10)
    recommended_game_ids.numpy()
    
    filtered_recommendations_ids = recommended_game_ids[recommended_game_ids != user_input_game_id]
    
    # Filter the DataFrame where 'game_id' is in the given array
    filtered_games = df_complete[df_complete['game_id'].isin(filtered_recommendations_ids.numpy())]
    
    # Extract the 'name' column (game names)
    game_names = filtered_games['name'].tolist()

    # Print the result
    print(game_names)
    print("Recommended Boardgames:", filtered_recommendations_ids.numpy())
   
    return filtered_recommendations_ids.numpy(), game_names, query_features


