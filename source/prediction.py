import tensorflow as tf
import tensorflow_recommenders as tfrs
from model import BoardgameContentModel 
from model_utils import create_retrieval_index, get_recommendation, create_input_df, preprocess_data, load_data


DATA_PATH = 'data/game_details_cleaned.csv'
CANDIDATE_DS_PATH = 'models/candidate_dataset'
WEIGHTS_PATH = 'models/board_game_model_weights/boardgame_model_weights'
EMBEDDING_DIM = 32


def load_model(candidate_dataset):
    model = BoardgameContentModel(EMBEDDING_DIM, candidate_dataset)
    try:
        status = model.load_weights(WEIGHTS_PATH)
        status.expect_partial()  # Tell TensorFlow you expect some missing/unrestored values.
        print("✅ Weights loaded successfully!")
    except Exception as e:
        print("⚠️ No saved weights found. Train the model first.")
        raise e
    return model


def recommend(game_query: str):
    # Load and preprocess data
    df_complete = load_data(DATA_PATH)
    df_features, df_game_ids, feature_list = preprocess_data(df_complete)
    df_input = create_input_df(df_complete, feature_list)

    # Load candidate dataset
    candidate_dataset = tf.data.experimental.load(CANDIDATE_DS_PATH)
    print("✅ Candidate dataset loaded successfully!")

    # Load model and create retrieval index
    model = load_model(candidate_dataset)
    index = create_retrieval_index(model, candidate_dataset)

    # Get recommendations
    return get_recommendation(game_query, df_complete, df_input, index)

if __name__ == "__main__":
    # Example usage:
    game_ids, game_names, query_features = recommend('Bingo')
    print("Recommendations:")
    print("IDs:", game_ids)
    print("Names:", game_names)
    # print("Query features:", query_features)





# df_complete = load_data(DATA_PATH)

# (df_features, df_game_ids, feature_list) = preprocess_data(df_complete)

# df_input = create_input_df(df_complete, feature_list)
 
#   # Load the dataset
# candidate_dataset = tf.data.experimental.load(CANDIDATE_DS_PATH)
# print("✅ Candidate dataset loaded successfully!")

# embedding_dim = 32

# model = BoardgameContentModel(embedding_dim, candidate_dataset)

# import os

# weights_index = "models/board_game_model_weights/boardgame_model_weights.index"
# data_file = "models/board_game_model_weights/boardgame_model_weights.data-00000-of-00001"

# print("Index file exists:", os.path.exists(weights_index))
# print("Data file exists:", os.path.exists(data_file))

# # Optionally, try to open the files in binary mode
# with open(weights_index, "rb") as f:
#     print("Successfully opened index file.")
# with open(data_file, "rb") as f:
#     print("Successfully opened data file.")


# # Load weights into the model
# try:
#     model.load_weights(WEIGHTS_PATH)
#     print("✅ Weights loaded successfully!")
# except:
#     print("⚠️ No saved weights found. Train the model first.")
    
# index = create_retrieval_index(model, candidate_dataset)


# game_ids, game_names, query_features = get_recommendation('Gloomhaven', df_complete, df_input, index)