"""
Content-Based Filtering recommender using pin metadata.
Builds a TF-IDF profile from category, subcategory, and tags,
then matches pins to user preference profiles.
"""

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


INTERACTION_WEIGHTS = {
    'save': 5,
    'like': 3,
    'click': 2,
    'share': 4,
    'comment': 1,
}


class ContentBasedRecommender:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=500, stop_words='english')
        self.pin_vectors = None
        self.pin_ids = None
        self.pin_index = None
        self.pins_df = None

    def fit(self, pins_df, interactions_df):
        """Build TF-IDF vectors from pin content and index user interactions."""
        self.pins_df = pins_df.copy()
        self.interactions_df = interactions_df.copy()
        self.interactions_df['weight'] = (
            self.interactions_df['interaction_type']
            .map(INTERACTION_WEIGHTS).fillna(1)
        )

        # Build content string per pin: category + subcategory + tags
        def build_content(row):
            parts = [
                str(row.get('category', '')),
                str(row.get('subcategory', '')),
                str(row.get('tags', '')),
            ]
            return ' '.join(parts).lower()

        self.pins_df['content'] = self.pins_df.apply(build_content, axis=1)
        self.pin_ids = self.pins_df['pin_id'].values
        self.pin_index = {p: i for i, p in enumerate(self.pin_ids)}

        self.pin_vectors = self.vectorizer.fit_transform(self.pins_df['content'])
        return self

    def _get_user_profile(self, user_id):
        """Build a weighted TF-IDF profile from a user's interaction history."""
        user_interactions = self.interactions_df[
            self.interactions_df['user_id'] == user_id
        ]
        if user_interactions.empty:
            return None

        profile = np.zeros(self.pin_vectors.shape[1])
        total_weight = 0
        for _, row in user_interactions.iterrows():
            if row['pin_id'] in self.pin_index:
                idx = self.pin_index[row['pin_id']]
                weight = row['weight']
                profile += weight * self.pin_vectors[idx].toarray().flatten()
                total_weight += weight

        return profile / total_weight if total_weight > 0 else None

    def recommend(self, user_id, n=10, exclude_seen=True):
        """Return top-N pins by content similarity to user's preference profile."""
        profile = self._get_user_profile(user_id)
        if profile is None:
            return []

        scores = cosine_similarity([profile], self.pin_vectors).flatten()

        if exclude_seen:
            seen_pins = set(
                self.interactions_df[self.interactions_df['user_id'] == user_id]['pin_id']
            )
            for pin_id in seen_pins:
                if pin_id in self.pin_index:
                    scores[self.pin_index[pin_id]] = 0

        top_pins = np.argsort(scores)[::-1][:n]
        return [self.pin_ids[i] for i in top_pins]