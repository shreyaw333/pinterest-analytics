import os
import sys
import django
import pandas as pd
from datetime import datetime
import json
import ast

# Add the project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pinterest_recommender.settings')
django.setup()

from apps.core.models import User, Board, Pin, UserInteraction, SearchQuery

def load_users():
    """Load users from CSV"""
    print("Loading users...")
    df = pd.read_csv('data/raw/pinterest_users.csv')
    
    users_created = 0
    for _, row in df.iterrows():
        try:
            # Safely parse preferred_categories from string to list
            preferred_cats = []
            if pd.notna(row['preferred_categories']):
                try:
                    preferred_cats = ast.literal_eval(row['preferred_categories'])
                except:
                    preferred_cats = []
            
            # Skip if user already exists
            if User.objects.filter(email=row['email']).exists():
                continue
            
            user = User.objects.create_user(
                username=row['username'],
                email=row['email'],
                first_name=row['first_name'],
                last_name=row['last_name'],
                password='defaultpassword123'  # Set a default password
            )
            
            # Update additional fields
            user.bio = row['bio'] if pd.notna(row['bio']) else None
            user.location = row['location']
            user.followers_count = int(row['followers_count'])
            user.following_count = int(row['following_count'])
            user.boards_count = int(row['boards_count'])
            user.pins_count = int(row['pins_count'])
            user.account_type = row['account_type']
            user.is_verified = bool(row['is_verified'])
            user.preferred_categories = preferred_cats
            user.save()
            
            users_created += 1
            if users_created % 100 == 0:
                print(f"  Created {users_created} users...")
                
        except Exception as e:
            print(f"Error creating user {row.get('username', 'unknown')}: {e}")
            continue
    
    print(f"Created {users_created} users")
    return User.objects.all()

def load_boards(users):
    """Load boards from CSV"""
    print("Loading boards...")
    df = pd.read_csv('data/raw/pinterest_boards.csv')
    
    # Create a mapping of user_id to User objects by email (since we don't have user_id in User model)
    user_emails = {row['user_id']: row['email'] for _, row in pd.read_csv('data/raw/pinterest_users.csv').iterrows()}
    user_map = {user_id: User.objects.filter(email=user_emails.get(user_id)).first() 
                for user_id in user_emails.keys()}
    
    boards_created = 0
    for _, row in df.iterrows():
        try:
            user = user_map.get(row['user_id'])
            if not user:
                continue
            
            # Skip if board already exists for this user with this title
            if Board.objects.filter(user=user, title=row['title']).exists():
                continue
                
            board = Board.objects.create(
                user=user,
                title=row['title'],
                description=row['description'] if pd.notna(row['description']) else None,
                category=row['category'],
                subcategory=row['subcategory'],
                is_private=bool(row['is_private']),
                pins_count=int(row['pins_count']),
                followers_count=int(row['followers_count']),
            )
            
            boards_created += 1
            if boards_created % 500 == 0:
                print(f"  Created {boards_created} boards...")
                
        except Exception as e:
            print(f"Error creating board {row.get('title', 'unknown')}: {e}")
            continue
    
    print(f"Created {boards_created} boards")
    return Board.objects.all()

def load_pins(boards):
    """Load pins from CSV"""
    print("Loading pins...")
    df = pd.read_csv('data/raw/pinterest_pins.csv')
    
    # Create mapping of board_id to actual board objects
    board_ids = pd.read_csv('data/raw/pinterest_boards.csv')
    board_map = {}
    for _, board_row in board_ids.iterrows():
        board_obj = Board.objects.filter(
            title=board_row['title'], 
            user__email__in=pd.read_csv('data/raw/pinterest_users.csv')[
                pd.read_csv('data/raw/pinterest_users.csv')['user_id'] == board_row['user_id']
            ]['email'].values
        ).first()
        if board_obj:
            board_map[board_row['board_id']] = board_obj
    
    pins_created = 0
    for _, row in df.iterrows():
        try:
            board = board_map.get(row['board_id'])
            if not board:
                continue
            
            # Skip if pin already exists
            if Pin.objects.filter(title=row['title'], user=board.user).exists():
                continue
            
            # Parse JSON fields safely
            color_palette = []
            tags = []
            
            if pd.notna(row['color_palette']):
                try:
                    color_palette = ast.literal_eval(row['color_palette'])
                except:
                    color_palette = []
                    
            if pd.notna(row['tags']):
                try:
                    tags = ast.literal_eval(row['tags'])
                except:
                    tags = []
            
            pin = Pin.objects.create(
                board=board,
                user=board.user,
                title=row['title'],
                description=row['description'] if pd.notna(row['description']) else None,
                image_url=row['image_url'],
                source_url=row['source_url'] if pd.notna(row['source_url']) else None,
                category=row['category'],
                subcategory=row['subcategory'],
                width=int(row['width']),
                height=int(row['height']),
                color_palette=color_palette,
                saves_count=int(row['saves_count']),
                likes_count=int(row['likes_count']),
                comments_count=int(row['comments_count']),
                shares_count=int(row['shares_count']),
                clicks_count=int(row['clicks_count']),
                impressions_count=int(row['impressions_count']),
                trending_score=float(row['trending_score']),
                is_promoted=bool(row['is_promoted']),
                tags=tags,
            )
            
            pins_created += 1
            if pins_created % 1000 == 0:
                print(f"  Created {pins_created} pins...")
                
        except Exception as e:
            print(f"Error creating pin {row.get('title', 'unknown')}: {e}")
            continue
    
    print(f"Created {pins_created} pins")
    return Pin.objects.all()

def load_interactions(users, pins):
    """Load user interactions from CSV"""
    print("Loading interactions...")
    df = pd.read_csv('data/raw/pinterest_interactions.csv')
    
    # Create mappings
    user_map = {str(user.user_id): user for user in users}
    pin_map = {str(pin.pin_id): pin for pin in pins}
    
    interactions_created = 0
    for _, row in df.iterrows():
        try:
            user = user_map.get(row['user_id'])
            pin = pin_map.get(row['pin_id'])
            
            if not user or not pin:
                continue
            
            session_id = row['session_id'] if pd.notna(row['session_id']) else None
            
            interaction, created = UserInteraction.objects.get_or_create(
                user=user,
                pin=pin,
                interaction_type=row['interaction_type'],
                defaults={
                    'session_id': session_id,
                    'device_type': row['device_type'],
                    'referrer': row['referrer'],
                }
            )
            if created:
                interactions_created += 1
                
        except Exception as e:
            print(f"Error creating interaction: {e}")
            continue
    
    print(f"Created {interactions_created} interactions")

def load_search_queries(users):
    """Load search queries from CSV"""
    print("Loading search queries...")
    df = pd.read_csv('data/raw/pinterest_searches.csv')
    
    user_map = {str(user.user_id): user for user in users}
    
    queries_created = 0
    for _, row in df.iterrows():
        try:
            user = user_map.get(row['user_id'])
            if not user:
                continue
            
            session_id = row['session_id'] if pd.notna(row['session_id']) else None
            
            query, created = SearchQuery.objects.get_or_create(
                user=user,
                query_text=row['query_text'],
                defaults={
                    'results_count': row['results_count'],
                    'clicked_results': row['clicked_results'],
                    'session_id': session_id,
                }
            )
            if created:
                queries_created += 1
                
        except Exception as e:
            print(f"Error creating search query: {e}")
            continue
    
    print(f"Created {queries_created} search queries")

def main():
    """Load all CSV data into Django models"""
    print("Starting data loading process...")
    print(f"Current working directory: {os.getcwd()}")
    
    # Check if data files exist
    data_files = [
        'data/raw/pinterest_users.csv',
        'data/raw/pinterest_boards.csv', 
        'data/raw/pinterest_pins.csv',
        'data/raw/pinterest_interactions.csv',
        'data/raw/pinterest_searches.csv'
    ]
    
    for file_path in data_files:
        if not os.path.exists(file_path):
            print(f"Error: {file_path} not found!")
            return
    
    # Load data in order (respecting foreign key relationships)
    users = load_users()
    boards = load_boards(users)
    pins = load_pins(boards)
    load_interactions(users, pins)
    load_search_queries(users)
    
    # Print summary
    print("\nData loading complete!")
    print(f"Total users: {User.objects.count()}")
    print(f"Total boards: {Board.objects.count()}")
    print(f"Total pins: {Pin.objects.count()}")
    print(f"Total interactions: {UserInteraction.objects.count()}")
    print(f"Total search queries: {SearchQuery.objects.count()}")

if __name__ == "__main__":
    main()