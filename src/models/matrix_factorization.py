"""
Matrix Factorization recommender using Truncated SVD.
Decomposes the user-item interaction matrix into latent factors
to discover hidden preference patterns.
"""

import numpy as np
import pandas as pd
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import normalize
from scipy.sparse import csr_matrix

INTERACTION_WEIGHTS = {
    'save': 5,
    'like': 3,
    'click': 2,
    'share': 4,
    'comment': 1,
}


class MatrixFactorizationRecommender:
    def __init__(self, n_factors=50, n_iterations=20):
        self.n_factors = n_factors
        self.n_iterations = n_iterations
        self.svd = TruncatedSVD(n_components=n_factors, n_iter=n_iterations, random_state=42)
        self.user_factors = None
        self.item_factors = None
        self.user_index = None
        self.pin_index = None
        self.user_ids = None
        self.pin_ids = None
        self.user_item_matrix = None

    def fit(self, interactions_df):
        """Fit SVD on weighted user-item matrix."""
        df = interactions_df.copy()
        df['weight'] = df['interaction_type'].map(INTERACTION_WEIGHTS).fillna(1)
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

        # Decompose: user_factors @ item_factors.T ≈ user_item_matrix
        self.user_factors = self.svd.fit_transform(self.user_item_matrix)
        self.item_factors = self.svd.components_.T  # shape: (n_pins, n_factors)

        # Normalize for stable dot products
        self.user_factors = normalize(self.user_factors)
        self.item_factors = normalize(self.item_factors)
        return self

    def recommend(self, user_id, n=10, exclude_seen=True):
        """Return top-N pin recommendations using latent factor dot products."""
        if user_id not in self.user_index:
            return []

        u_idx = self.user_index[user_id]
        scores = self.user_factors[u_idx] @ self.item_factors.T

        if exclude_seen:
            seen = self.user_item_matrix[u_idx].toarray().flatten()
            scores[seen > 0] = 0

        top_pins = np.argsort(scores)[::-1][:n]
        return [self.pin_ids[i] for i in top_pins]

    def get_explained_variance(self):
        return float(np.sum(self.svd.explained_variance_ratio_))