import pandas as pd
from faker import Faker
import random
import numpy as np
from datetime import datetime, timedelta
import uuid
import json
import os

fake = Faker()
Faker.seed(42)
random.seed(42)
np.random.seed(42)

# Pinterest-style categories and subcategories
CATEGORIES = {
    'Fashion': ['Outfit Ideas', 'Shoes', 'Accessories', 'Makeup', 'Hair Styles', 'Wedding Dresses'],
    'Home Decor': ['Living Room', 'Kitchen', 'Bedroom', 'Bathroom', 'DIY Projects', 'Organization'],
    'Food': ['Recipes', 'Desserts', 'Healthy Eating', 'Meal Prep', 'Baking', 'Cocktails'],
    'Travel': ['Destinations', 'Travel Tips', 'Photography', 'Road Trips', 'Hotels', 'Adventure'],
    'DIY & Crafts': ['Art Projects', 'Crafts', 'Woodworking', 'Sewing', 'Upcycling', 'Handmade'],
    'Beauty': ['Skincare', 'Makeup Tutorials', 'Nail Art', 'Hair Care', 'Beauty Tips', 'Natural Beauty'],
    'Health & Fitness': ['Workout Routines', 'Yoga', 'Running', 'Nutrition', 'Mental Health', 'Weight Loss'],
    'Photography': ['Portrait', 'Landscape', 'Wedding', 'Street', 'Nature', 'Black & White'],
    'Art': ['Paintings', 'Drawings', 'Digital Art', 'Sculptures', 'Mixed Media', 'Street Art'],
    'Gardening': ['Indoor Plants', 'Garden Design', 'Vegetable Gardens', 'Flowers', 'Landscaping', 'Herbs']
}

def generate_users(num_users=2000):
    """Generate realistic user data - REDUCED SIZE"""
    users = []
    
    print(f"Generating {num_users} users...")
    for i in range(num_users):
        if i % 500 == 0:
            print(f"  Generated {i} users...")
            
        user = {
            'user_id': str(uuid.uuid4()),
            'username': fake.user_name(),
            'email': fake.email(),
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'bio': fake.text(max_nb_chars=150) if random.random() > 0.3 else None,
            'location': fake.city() + ', ' + fake.state_abbr(),
            'followers_count': max(0, int(np.random.exponential(100))),
            'following_count': max(0, int(np.random.exponential(150))),
            'boards_count': random.randint(1, 25),
            'pins_count': max(0, int(np.random.exponential(50))),
            'account_type': random.choices(['personal', 'business'], weights=[0.8, 0.2])[0],
            'created_at': fake.date_time_between(start_date='-3y', end_date='now'),
            'last_active': fake.date_time_between(start_date='-30d', end_date='now'),
            'is_verified': random.choices([True, False], weights=[0.05, 0.95])[0],
            'preferred_categories': random.sample(list(CATEGORIES.keys()), k=random.randint(2, 5))
        }
        users.append(user)
    
    return pd.DataFrame(users)

def generate_boards(users_df, avg_boards_per_user=3):
    """Generate boards for users - REDUCED SIZE"""
    boards = []
    
    print(f"Generating boards for {len(users_df)} users...")
    for i, (_, user) in enumerate(users_df.iterrows()):
        if i % 500 == 0:
            print(f"  Processed {i} users...")
            
        num_boards = max(1, int(np.random.poisson(avg_boards_per_user)))
        
        for _ in range(num_boards):
            category = random.choice(list(CATEGORIES.keys()))
            subcategory = random.choice(CATEGORIES[category])
            
            board = {
                'board_id': str(uuid.uuid4()),
                'user_id': user['user_id'],
                'title': f"{fake.catch_phrase()} - {subcategory}",
                'description': fake.text(max_nb_chars=200) if random.random() > 0.4 else None,
                'category': category,
                'subcategory': subcategory,
                'is_private': random.choices([True, False], weights=[0.15, 0.85])[0],
                'pins_count': max(0, int(np.random.exponential(20))),
                'followers_count': max(0, int(np.random.exponential(10))),
                'created_at': fake.date_time_between(start_date=user['created_at'], end_date='now'),
                'updated_at': fake.date_time_between(start_date=user['created_at'], end_date='now')
            }
            boards.append(board)
    
    return pd.DataFrame(boards)

def generate_pins(boards_df, avg_pins_per_board=8):
    """Generate pins for boards - REDUCED SIZE"""
    pins = []
    image_dimensions = [(736, 1104), (564, 752), (474, 711), (600, 900), (640, 960)]
    
    print(f"Generating pins for {len(boards_df)} boards...")
    for i, (_, board) in enumerate(boards_df.iterrows()):
        if i % 1000 == 0:
            print(f"  Processed {i} boards...")
            
        num_pins = max(1, int(np.random.poisson(avg_pins_per_board)))
        
        for _ in range(num_pins):
            width, height = random.choice(image_dimensions)
            
            days_since_created = (datetime.now() - fake.date_time_between(
                start_date=board['created_at'], end_date='now'
            )).days
            
            base_trending_score = max(0, 100 - (days_since_created * 0.5))
            trending_score = base_trending_score * random.uniform(0.1, 2.0)
            
            pin = {
                'pin_id': str(uuid.uuid4()),
                'board_id': board['board_id'],
                'user_id': board['user_id'],
                'title': fake.sentence(nb_words=random.randint(3, 8)).rstrip('.'),
                'description': fake.text(max_nb_chars=300) if random.random() > 0.3 else None,
                'image_url': fake.image_url(width=width, height=height),
                'source_url': fake.url() if random.random() > 0.4 else None,
                'category': board['category'],
                'subcategory': board['subcategory'],
                'width': width,
                'height': height,
                'color_palette': [fake.hex_color() for _ in range(random.randint(3, 6))],
                'saves_count': max(0, int(np.random.exponential(50))),
                'likes_count': max(0, int(np.random.exponential(30))),
                'comments_count': max(0, int(np.random.exponential(5))),
                'shares_count': max(0, int(np.random.exponential(8))),
                'clicks_count': max(0, int(np.random.exponential(100))),
                'impressions_count': max(0, int(np.random.exponential(1000))),
                'trending_score': round(trending_score, 2),
                'is_promoted': random.choices([True, False], weights=[0.1, 0.9])[0],
                'tags': [fake.word() for _ in range(random.randint(2, 8))],
                'created_at': fake.date_time_between(start_date=board['created_at'], end_date='now'),
                'updated_at': fake.date_time_between(start_date=board['created_at'], end_date='now')
            }
            pins.append(pin)
    
    return pd.DataFrame(pins)

def generate_user_interactions_optimized(users_df, pins_df, num_interactions=10000):
    """Generate user interaction data - OPTIMIZED VERSION"""
    print(f"Generating {num_interactions} user interactions (optimized)...")
    
    # Pre-convert DataFrames to lists for faster sampling
    users_list = users_df.to_dict('records')
    pins_list = pins_df.to_dict('records')
    
    # Create category preference lookup for faster access
    user_preferences = {}
    for user in users_list:
        user_preferences[user['user_id']] = user['preferred_categories']
    
    interactions = []
    interaction_types = ['save', 'like', 'click', 'share', 'comment']
    
    for i in range(num_interactions):
        if i % 2000 == 0:
            print(f"  Generated {i} interactions...")
        
        # Randomly sample user and pin
        user = random.choice(users_list)
        pin = random.choice(pins_list)
        
        interaction_type = random.choices(
            interaction_types, 
            weights=[0.4, 0.25, 0.2, 0.1, 0.05]
        )[0]
        
        # Quick category preference check
        category_boost = 1.0
        if pin['category'] in user_preferences.get(user['user_id'], []):
            category_boost = 3.0
        
        if random.random() < (0.15 * category_boost):  # Slightly higher interaction probability
            interaction = {
                'interaction_id': str(uuid.uuid4()),
                'user_id': user['user_id'],
                'pin_id': pin['pin_id'],
                'interaction_type': interaction_type,
                'timestamp': fake.date_time_between(start_date='-90d', end_date='now'),
                'session_id': str(uuid.uuid4()) if random.random() > 0.7 else None,
                'device_type': random.choices(['mobile', 'desktop', 'tablet'], weights=[0.7, 0.25, 0.05])[0],
                'referrer': random.choices(['home_feed', 'search', 'category_browse', 'related_pins'], 
                                         weights=[0.4, 0.3, 0.2, 0.1])[0]
            }
            interactions.append(interaction)
    
    return pd.DataFrame(interactions)

def generate_search_queries(users_df, num_queries=5000):
    """Generate search query data - REDUCED SIZE"""
    queries = []
    
    search_terms = [
        'outfit ideas', 'home decor', 'wedding dress', 'healthy recipes', 'workout routine',
        'diy projects', 'travel destinations', 'makeup tutorial', 'bedroom decor', 'hair styles',
        'nail art', 'garden ideas', 'photography tips', 'art inspiration', 'fashion trends'
    ]
    
    users_list = users_df.to_dict('records')
    
    print(f"Generating {num_queries} search queries...")
    for i in range(num_queries):
        if i % 1000 == 0:
            print(f"  Generated {i} queries...")
            
        user = random.choice(users_list)
        
        query = {
            'query_id': str(uuid.uuid4()),
            'user_id': user['user_id'],
            'query_text': random.choice(search_terms) + (' ' + fake.word() if random.random() > 0.5 else ''),
            'timestamp': fake.date_time_between(start_date='-90d', end_date='now'),
            'results_count': random.randint(10, 1000),
            'clicked_results': random.randint(0, 5),
            'session_id': str(uuid.uuid4())
        }
        queries.append(query)
    
    return pd.DataFrame(queries)

def main():
    """Generate all Pinterest data - OPTIMIZED VERSION"""
    print("Generating Pinterest-like data (optimized for speed)...")
    print("Reduced dataset size for faster generation and testing")
    
    os.makedirs('../../data/raw', exist_ok=True)
    
    # Generate data with smaller sizes
    users_df = generate_users(2000)  # Reduced from 10000
    boards_df = generate_boards(users_df)
    pins_df = generate_pins(boards_df)
    interactions_df = generate_user_interactions_optimized(users_df, pins_df, 10000)  # Reduced from 100000
    search_df = generate_search_queries(users_df, 5000)  # Reduced from 20000
    
    # Save to CSV files
    print("\nSaving data to CSV files...")
    users_df.to_csv('../../data/raw/pinterest_users.csv', index=False)
    boards_df.to_csv('../../data/raw/pinterest_boards.csv', index=False)
    pins_df.to_csv('data/raw/pinterest_pins.csv', index=False)
    interactions_df.to_csv('data/raw/pinterest_interactions.csv', index=False)
    search_df.to_csv('data/raw/pinterest_searches.csv', index=False)
    
    # Summary statistics
    print("\nData Generation Summary:")
    print(f"Users: {len(users_df):,}")
    print(f"Boards: {len(boards_df):,}")
    print(f"Pins: {len(pins_df):,}")
    print(f"Interactions: {len(interactions_df):,}")
    print(f"Search Queries: {len(search_df):,}")
    
    print(f"\nSample Statistics:")
    print(f"Average pins per user: {pins_df.groupby('user_id').size().mean():.1f}")
    print(f"Average saves per pin: {pins_df['saves_count'].mean():.1f}")
    print(f"Most popular category: {pins_df['category'].mode()[0]}")
    print(f"Average trending score: {pins_df['trending_score'].mean():.2f}")
    
    print("\nSample Pin Data:")
    print(pins_df[['title', 'category', 'saves_count', 'trending_score']].head())
    
    print("\nData generation complete! Files saved in data/raw/:")
    for file in ['pinterest_users.csv', 'pinterest_boards.csv', 'pinterest_pins.csv', 
                 'pinterest_interactions.csv', 'pinterest_searches.csv']:
        print(f"- {file}")
    
    # Save metadata
    metadata = {
        'generation_date': datetime.now().isoformat(),
        'total_users': len(users_df),
        'total_boards': len(boards_df),
        'total_pins': len(pins_df),
        'total_interactions': len(interactions_df),
        'total_searches': len(search_df),
        'categories': list(CATEGORIES.keys()),
        'optimization': 'reduced_size_for_speed'
    }
    
    with open('data/raw/generation_metadata.json', 'w') as f:
        json.dump(metadata, f, indent=2)

if __name__ == "__main__":
    main()