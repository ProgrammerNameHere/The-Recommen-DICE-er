
import tensorflow as tf
import tensorflow_recommenders as tfrs


# Define the BoardgameContentModel class
class BoardgameContentModel(tfrs.Model):
    # Initialize the parent tfrs.Model class.
    def __init__(self, embedding_dim, candidate_dataset):
        super().__init__()
        
        # Build the boardgame feature encoder (tower)
        # - Input: Feature vector with length equal to number of feature_names
        # - Hidden layer: 64 neurons with ReLU activation
        # - Output layer: Projects to the embedding space of dimension `embedding_dim`
        # - Normalization: L2 normalization for cosine similarity      
        self.boardgame_model = tf.keras.Sequential([
            tf.keras.layers.InputLayer(input_shape=(280,)),
            tf.keras.layers.Dense(64, activation='relu'),
            tf.keras.layers.Dense(embedding_dim),
            tf.keras.layers.Lambda(lambda x: tf.math.l2_normalize(x, axis=1))
        ])
        
        # Precompute candidate embeddings from the candidate dataset
        # Each candidate is expected to be a dictionary with a features key    
        candidate_embeddings = candidate_dataset.map(
            lambda x: self.boardgame_model(x["features"])
        )
        
        # Configure the retrieval task with FactorizedTopK metrics using the candidate embeddings
        self.task = tfrs.tasks.Retrieval(
            metrics=tfrs.metrics.FactorizedTopK(candidates=candidate_embeddings)
        )
    
    
    # The compute_loss method defines how the model's loss is computed during training
    def compute_loss(self, features, training=False):
        # Compute boardgame embeddings from the input features.
        boardgame_embeddings = self.boardgame_model(features["features"])
        
        # Use the embeddings as both query and candidate for the retrieval task
        # The task computes a loss based on ranking similar items higher    
        return self.task(boardgame_embeddings, boardgame_embeddings)