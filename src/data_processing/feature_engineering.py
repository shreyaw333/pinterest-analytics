import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import csr_matrix
import pickle
import os

class FeatureEngineer:
    def __init__(self, data_path='data/raw/'):
        self.data_path = data_path
        self.users_df = None
        self.pins_df = None
        self.interactions_df = None
        
    def load_data(self):
        """Load all CSV files"""
        print("Loading data...")
        self.users_df = pd.read_csv(f'{self.data_path}pinterest_users.csv')
        self.pins_df = pd.read_csv(f'{self.data_path}pinterest_pins.csv')
        self.interactions_df = pd.read_csv(f'{self.data_path}pinterest_interactions.csv')
        
        print(f"Loaded {len(self.users_df)} users, {len(self.pins_df)} pins, {len(self.interactions_df)} interactions")
        
    def create_user_item_matrix(self):
        """Create user-item interaction matrix for collaborative filtering"""
        print("Creating user-item matrix...")
        
        # Create interaction weights (saves worth more than clicks)
        interaction_weights = {
            'save': 5,
            'like': 3,
            'share': 4,
            'click': 1,
            'comment': 2
        }
        
        # Add weights to interactions
        self.interactions_df['weight'] = self.interactions_df['interaction_type'].map(interaction_weights)
        
        # Create pivot table
        user_item_matrix = self.interactions_df.pivot_table(
            index='user_id',
            columns='pin_id', 
            values='weight',
            fill_value=0
        )
        
        print(f"User-item matrix shape: {user_item_matrix.shape}")
        return user_item_matrix.astype(np.float32)
        
    def create_user_profiles(self):
        """Create user preference profiles based on interactions"""
        print("Creating user profiles...")
        
        # Get user interactions with pin categories
        user_interactions = self.interactions_df.merge(
            self.pins_df[['pin_id', 'category', 'trending_score', 'saves_count']], 
            on='pin_id'
        )
        
        # Calculate category preferences
        category_preferences = user_interactions.groupby(['user_id', 'category']).agg({
            'interaction_type': 'count',
            'trending_score': 'mean',
            'saves_count': 'mean'
        }).reset_index()
        
        # Normalize preferences by user
        category_preferences['preference_score'] = (
            category_preferences.groupby('user_id')['interaction_type']
            .transform(lambda x: x / x.sum())
        )
        
        # Create user profile vectors
        user_profiles = category_preferences.pivot_table(
            index='user_id',
            columns='category',
            values='preference_score',
            fill_value=0
        )
        
        print(f"User profiles shape: {user_profiles.shape}")
        return user_profiles
        
    def create_pin_features(self):
        """Create pin feature vectors for content-based filtering"""
        print("Creating pin features...")
        
        # Combine text features
        self.pins_df['text_features'] = (
            self.pins_df['title'].fillna('') + ' ' + 
            self.pins_df['description'].fillna('') + ' ' +
            self.pins_df['category'] + ' ' +
            self.pins_df['subcategory']
        )
        
        # Create TF-IDF vectors
        tfidf = TfidfVectorizer(max_features=1000, stop_words='english')
        text_features = tfidf.fit_transform(self.pins_df['text_features'])
        
        # Normalize numerical features
        numerical_features = self.pins_df[['trending_score', 'saves_count', 'likes_count', 'width', 'height']].fillna(0)
        numerical_features = (numerical_features - numerical_features.mean()) / numerical_features.std()
        
        print(f"Pin features - Text: {text_features.shape}, Numerical: {numerical_features.shape}")
        
        return {
            'text_features': text_features,
            'numerical_features': numerical_features.values,
            'tfidf_vectorizer': tfidf
        }
        
    def calculate_pin_similarities(self, pin_features):
        """Calculate pin-to-pin similarity matrix"""
        print("Calculating pin similarities...")
        
        # Combine text and numerical features (weighted)
        text_weight = 0.7
        num_weight = 0.3
        
        # Normalize and combine features
        from sklearn.preprocessing import normalize
        text_norm = normalize(pin_features['text_features'])
        num_norm = normalize(pin_features['numerical_features'])
        
        # Calculate similarities
        text_sim = cosine_similarity(text_norm)
        num_sim = cosine_similarity(num_norm)
        
        # Weighted combination
        pin_similarity = text_weight * text_sim + num_weight * num_sim
        
        print(f"Pin similarity matrix shape: {pin_similarity.shape}")
        return pin_similarity
        
    def calculate_trending_scores(self):
        """Update trending scores based on recent interactions"""
        print("Calculating trending scores...")
        
        # Convert timestamp to datetime
        self.interactions_df['timestamp'] = pd.to_datetime(self.interactions_df['timestamp'])
        
        # Recent interactions (last 7 days)
        recent_cutoff = self.interactions_df['timestamp'].max() - pd.Timedelta(days=7)
        recent_interactions = self.interactions_df[self.interactions_df['timestamp'] > recent_cutoff]
        
        # Calculate recent engagement
        recent_engagement = recent_interactions.groupby('pin_id').agg({
            'interaction_type': 'count',
            'timestamp': 'max'
        }).reset_index()
        
        recent_engagement.columns = ['pin_id', 'recent_interactions', 'last_interaction']
        
        # Merge with pin data
        pins_with_trending = self.pins_df.merge(recent_engagement, on='pin_id', how='left')
        pins_with_trending['recent_interactions'] = pins_with_trending['recent_interactions'].fillna(0)
        
        # Calculate new trending score
        pins_with_trending['trending_score_updated'] = (
            pins_with_trending['saves_count'] * 0.4 +
            pins_with_trending['recent_interactions'] * 0.6 +
            pins_with_trending['trending_score'] * 0.2
        )
        
        return pins_with_trending[['pin_id', 'trending_score_updated']]
        
    def save_features(self, user_item_matrix, user_profiles, pin_features, pin_similarity, trending_scores):
        """Save all engineered features"""
        print("Saving engineered features...")
        
        os.makedirs('data/processed/', exist_ok=True)
        
        # Save matrices
        np.save('data/processed/user_item_matrix.npy', user_item_matrix.values)
        np.save('data/processed/user_profiles.npy', user_profiles.values)
        np.save('data/processed/pin_similarity.npy', pin_similarity)
        
        # Save feature mappings
        feature_mappings = {
            'user_ids': user_item_matrix.index.tolist(),
            'pin_ids': user_item_matrix.columns.tolist(),
            'user_profile_ids': user_profiles.index.tolist(),
            'categories': user_profiles.columns.tolist(),
            'pin_feature_ids': self.pins_df['pin_id'].tolist()
        }
        
        with open('data/processed/feature_mappings.pkl', 'wb') as f:
            pickle.dump(feature_mappings, f)
            
        # Save TF-IDF vectorizer
        with open('data/processed/tfidf_vectorizer.pkl', 'wb') as f:
            pickle.dump(pin_features['tfidf_vectorizer'], f)
            
        # Save trending scores
        trending_scores.to_csv('data/processed/trending_scores.csv', index=False)
        
        print("Features saved successfully!")
        
    def run_feature_engineering(self):
        """Main feature engineering pipeline"""
        print("Starting feature engineering pipeline...")
        
        # Load data
        self.load_data()
        
        # Create features
        user_item_matrix = self.create_user_item_matrix()
        user_profiles = self.create_user_profiles()
        pin_features = self.create_pin_features()
        pin_similarity = self.calculate_pin_similarities(pin_features)
        trending_scores = self.calculate_trending_scores()
        
        # Save features
        self.save_features(user_item_matrix, user_profiles, pin_features, pin_similarity, trending_scores)
        
        print("Feature engineering complete!")
        return {
            'user_item_matrix': user_item_matrix,
            'user_profiles': user_profiles,
            'pin_features': pin_features,
            'pin_similarity': pin_similarity,
            'trending_scores': trending_scores
        }

if __name__ == "__main__":
    engineer = FeatureEngineer()
    features = engineer.run_feature_engineering()