import tensorflow as tf
import tensorflow_recommenders as tfrs
from model import BoardgameContentModel 
from model_utils import create_retrieval_index, get_recommendation, create_input_df, preprocess_data, load_data
import streamlit as st

DATA_PATH = 'data/game_details_cleaned.csv'
CANDIDATE_DS_PATH = 'models/candidate_dataset'
WEIGHTS_PATH = 'models/board_game_model_weights/boardgame_model_weights'
EMBEDDING_DIM = 32


@st.cache_resource
def load_model(_candidate_dataset):
    model = BoardgameContentModel(EMBEDDING_DIM, _candidate_dataset)
    try:
        status = model.load_weights(WEIGHTS_PATH)
        status.expect_partial()  # Tell TensorFlow you expect some missing/unrestored values.
        print("✅ Weights loaded successfully!")
    except Exception as e:
        print("⚠️ No saved weights found. Train the model first.")
        raise e
    return model


@st.cache_resource
def load_candidates(CANDIDATE_DS_PATH):
    # Load candidate dataset
    candidate_dataset = tf.data.experimental.load(CANDIDATE_DS_PATH)
    print("✅ Candidate dataset loaded successfully!")
    return candidate_dataset

def recommend(game_query: str):
    # Load and preprocess data
    df_complete = load_data(DATA_PATH)
    df_features, df_game_ids, feature_list = preprocess_data(df_complete)
    df_input = create_input_df(df_complete, feature_list)

    # Load candidate dataset
    candidate_dataset = load_candidates(CANDIDATE_DS_PATH)

    # Load model and create retrieval index
    model = load_model(candidate_dataset)
    index = create_retrieval_index(model, candidate_dataset)

    # Get recommendations
    return get_recommendation(game_query, df_complete, df_input, index)

if __name__ == "__main__":
    # Example usage:
    game_ids, game_names, query_features = recommend(['Bingo', 'Gloomhaven'])
    print("Recommendations:")
    print("IDs:", game_ids)
    print("Names:", game_names)
    # print("Query features:", query_features)
