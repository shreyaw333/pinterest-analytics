"""
Collaborative Filtering recommender using user-item interaction matrix.
Computes user similarity via cosine similarity and recommends pins
that similar users have interacted with.
"""

import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import csr_matrix


# Interaction weights — saves are strongest signal, comments weakest
INTERACTION_WEIGHTS = {
    'save': 5,
    'like': 3,
    'click': 2,
    'share': 4,
    'comment': 1,
}


class CollaborativeFilteringRecommender:
    def __init__(self, n_similar_users=20):
        self.n_similar_users = n_similar_users
        self.user_item_matrix = None
        self.user_similarity = None
        self.user_ids = None
        self.pin_ids = None
        self.user_index = None
        self.pin_index = None

    def fit(self, interactions_df):
        """Build user-item matrix and compute user similarities."""
        df = interactions_df.copy()
        df['weight'] = df['interaction_type'].map(INTERACTION_WEIGHTS).fillna(1)

        # Aggregate weights per user-pin pair
        agg = df.groupby(['user_id', 'pin_id'])['weight'].sum().reset_index()

        self.user_ids = agg['user_id'].unique()
        self.pin_ids = agg['pin_id'].unique()
        self.user_index = {u: i for i, u in enumerate(self.user_ids)}
        self.pin_index = {p: i for i, p in enumerate(self.pin_ids)}

        rows = agg['user_id'].map(self.user_index)
        cols = agg['pin_id'].map(self.pin_index)
        data = agg['weight'].values

        self.user_item_matrix = csr_matrix(
            (data, (rows, cols)),
            shape=(len(self.user_ids), len(self.pin_ids))
        )

        # Cosine similarity between users
        self.user_similarity = cosine_similarity(self.user_item_matrix)
        return self

    def recommend(self, user_id, n=10, exclude_seen=True):
        """Return top-N pin recommendations for a given user."""
        if user_id not in self.user_index:
            return []

        u_idx = self.user_index[user_id]
        sim_scores = self.user_similarity[u_idx]

        # Weight item scores by similarity of top-N similar users
        top_users = np.argsort(sim_scores)[::-1][1:self.n_similar_users + 1]
        scores = np.zeros(len(self.pin_ids))
        for v_idx in top_users:
            scores += sim_scores[v_idx] * self.user_item_matrix[v_idx].toarray().flatten()

        if exclude_seen:
            seen = self.user_item_matrix[u_idx].toarray().flatten()
            scores[seen > 0] = 0

        top_pins = np.argsort(scores)[::-1][:n]
        return [self.pin_ids[i] for i in top_pins if scores[i] > 0]