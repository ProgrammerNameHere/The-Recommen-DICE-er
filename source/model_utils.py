import pandas as pd
import numpy as np
import tensorflow as tf
import tensorflow_recommenders as tfrs
from sklearn.model_selection import train_test_split
import matplotlib.cm as cm
import matplotlib.colors as mcolors

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
    scores, recommended_game_ids = index(aggregated_query_features, k=20)
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


def gradient_style(row, total_rows):
    """
    Returns a list of CSS styles for a row in a DataFrame,
    creating a gradient effect from the first row to the last row.
    
    Parameters:
    - row: A row of the DataFrame (with .name used as the index)
    - total_rows: Total number of rows in the DataFrame.
    
    For the first row (index 0), the background is light blue (rgb(173,216,230)).
    For the last row, the background is white (rgb(255,255,255)).
    """
    if total_rows > 10:
        total_rows = 10
    
    idx = row.name
    # Compute a factor that decreases linearly from 1 to 0
    factor = 1 - (idx / (total_rows - 1)) if total_rows > 1 else 1

    # Interpolate between light blue (173,216,230) and white (255,255,255)
    r = int(173 * factor + 255 * (1 - factor))
    g = int(216 * factor + 255 * (1 - factor))
    b = int(230 * factor + 255 * (1 - factor))
    
    # Return a style for each cell in this row
    return [f"background-color: rgb({r}, {g}, {b})" for _ in row]



def styled_scrollable_table(df, username_column="username", cmap_name="tab20c", max_height="400px"):
    """
    Styles a DataFrame by applying a unique background color to rows based on the user
    and wraps the table in a scrollable container.

    Parameters:
        df (pandas.DataFrame): The DataFrame to style.
        username_column (str): The column in the DataFrame that contains the username.
        cmap_name (str): The matplotlib colormap name to use for generating colors.
        max_height (str): The maximum height for the scrollable container (e.g., "400px").

    Returns:
        str: An HTML string of the styled, scrollable table.
    """
    # Generate a dynamic color mapping for unique users
    unique_users = df[username_column].unique()
    n_users = len(unique_users)
    cmap = cm.get_cmap(cmap_name, n_users)
    user_colors = {user: mcolors.to_hex(cmap(i)) for i, user in enumerate(unique_users)}
    
    # Define a helper function to style each row based on the username
    def color_by_user(row):
        user = row[username_column]
        color = user_colors.get(user, "#FFFFFF")  # fallback to white if user not found
        return [f"background-color: {color}"] * len(row)
    
    # Apply the styling to the DataFrame and convert to HTML
    styled_html = df.style.apply(lambda row: color_by_user(row), axis=1).to_html(index=False)
    
    # Wrap the styled table in a scrollable container
    scrollable_html = f"""
    <div style="overflow-x: auto; max-height: {max_height}; border: 1px solid #ccc; padding: 10px;">
        {styled_html}
    """
    return scrollable_html