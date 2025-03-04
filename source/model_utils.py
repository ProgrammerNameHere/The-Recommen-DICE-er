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
    # Append 'name' to feature_list if it is not already present
    if 'name' not in feature_list:
        feature_list.append('name')
    # Create df_input by selecting columns in the updated feature_list from df_complete
    df_input = df_complete[feature_list]
    
    return df_input


def get_recommendation(user_inputs, df_complete, df_input, index):
    # If the input is a single boardgame name (string), wrap it in a list.
    if isinstance(user_inputs, str):
        user_inputs = [user_inputs]
    
    # Retrieve the game IDs for all boardgames in the input.
    user_input_game_ids = df_complete.loc[df_complete['name'].isin(user_inputs), 'game_id'].values

    # Retrieve the feature vectors for each boardgame from your input DataFrame.
    # Assuming that all columns except the last one contain the features.
    query_features_list = df_input[df_input['name'].isin(user_inputs)].iloc[:, :-1].values.tolist()
    query_features_array = np.array(query_features_list)
    
    # Aggregate the multiple boardgame features by averaging.
    aggregated_query_features = np.mean(query_features_array, axis=0, keepdims=True)
    
    # Use the aggregated features to query the index for recommendations.
    scores, recommended_game_ids = index(aggregated_query_features, k=10)
    recommended_game_ids = recommended_game_ids.numpy()
    
    # Filter out any recommendations that are already part of the input.
    filtered_recommendations_ids = [
        game_id for game_id in recommended_game_ids[0]
        if game_id not in user_input_game_ids
    ]
    
    # Filter the complete DataFrame to get game names for the recommended IDs.
    filtered_games = df_complete[df_complete['game_id'].isin(filtered_recommendations_ids)]
    game_names = filtered_games['name'].tolist()
    
    # Print the result for debugging.
    print("Recommended Boardgames IDs:", filtered_recommendations_ids)
    print("Recommended Boardgames Names:", game_names)
    
    return filtered_recommendations_ids, game_names, aggregated_query_features