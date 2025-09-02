# apps/core/models_backup.py

from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

class User(AbstractUser):
    """Extended User model for Pinterest-like functionality"""
    user_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    bio = models.TextField(max_length=500, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True)
    followers_count = models.PositiveIntegerField(default=0)
    following_count = models.PositiveIntegerField(default=0)
    boards_count = models.PositiveIntegerField(default=0)
    pins_count = models.PositiveIntegerField(default=0)
    
    ACCOUNT_TYPES = [
        ('personal', 'Personal'),
        ('business', 'Business'),
    ]
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPES, default='personal')
    is_verified = models.BooleanField(default=False)
    preferred_categories = models.JSONField(default=list, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    last_active = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.username

class Board(models.Model):
    """Pinterest Board model"""
    board_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='boards')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    
    # Categories matching your generated data
    CATEGORIES = [
        ('Fashion', 'Fashion'),
        ('Home Decor', 'Home Decor'),
        ('Food', 'Food'),
        ('Travel', 'Travel'),
        ('DIY & Crafts', 'DIY & Crafts'),
        ('Beauty', 'Beauty'),
        ('Health & Fitness', 'Health & Fitness'),
        ('Photography', 'Photography'),
        ('Art', 'Art'),
        ('Gardening', 'Gardening'),
    ]
    
    category = models.CharField(max_length=50, choices=CATEGORIES)
    subcategory = models.CharField(max_length=100)
    is_private = models.BooleanField(default=False)
    pins_count = models.PositiveIntegerField(default=0)
    followers_count = models.PositiveIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} by {self.user.username}"

class Pin(models.Model):
    """Pinterest Pin model"""
    pin_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='pins')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pins')
    
    title = models.CharField(max_length=500)
    description = models.TextField(blank=True, null=True)
    image_url = models.URLField(max_length=500)
    source_url = models.URLField(max_length=500, blank=True, null=True)
    
    category = models.CharField(max_length=50, choices=Board.CATEGORIES)
    subcategory = models.CharField(max_length=100)
    
    # Image properties
    width = models.PositiveIntegerField()
    height = models.PositiveIntegerField()
    color_palette = models.JSONField(default=list, blank=True)
    
    # Engagement metrics
    saves_count = models.PositiveIntegerField(default=0)
    likes_count = models.PositiveIntegerField(default=0)
    comments_count = models.PositiveIntegerField(default=0)
    shares_count = models.PositiveIntegerField(default=0)
    clicks_count = models.PositiveIntegerField(default=0)
    impressions_count = models.PositiveIntegerField(default=0)
    
    # ML features
    trending_score = models.FloatField(default=0.0)
    is_promoted = models.BooleanField(default=False)
    tags = models.JSONField(default=list, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['category']),
            models.Index(fields=['trending_score']),
            models.Index(fields=['-created_at']),
            models.Index(fields=['saves_count']),
        ]
    
    def __str__(self):
        return self.title[:50]
    
    @property
    def engagement_rate(self):
        """Calculate engagement rate"""
        if self.impressions_count == 0:
            return 0
        total_engagement = self.saves_count + self.likes_count + self.clicks_count
        return (total_engagement / self.impressions_count) * 100

class UserInteraction(models.Model):
    """User interaction with pins"""
    interaction_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='interactions')
    pin = models.ForeignKey(Pin, on_delete=models.CASCADE, related_name='interactions')
    
    INTERACTION_TYPES = [
        ('save', 'Save'),
        ('like', 'Like'),
        ('click', 'Click'),
        ('share', 'Share'),
        ('comment', 'Comment'),
    ]
    
    interaction_type = models.CharField(max_length=20, choices=INTERACTION_TYPES)
    timestamp = models.DateTimeField(auto_now_add=True)
    session_id = models.UUIDField(blank=True, null=True)
    
    DEVICE_TYPES = [
        ('mobile', 'Mobile'),
        ('desktop', 'Desktop'),
        ('tablet', 'Tablet'),
    ]
    device_type = models.CharField(max_length=20, choices=DEVICE_TYPES)
    
    REFERRER_TYPES = [
        ('home_feed', 'Home Feed'),
        ('search', 'Search'),
        ('category_browse', 'Category Browse'),
        ('related_pins', 'Related Pins'),
    ]
    referrer = models.CharField(max_length=30, choices=REFERRER_TYPES)
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['user', 'interaction_type']),
            models.Index(fields=['pin', 'interaction_type']),
            models.Index(fields=['-timestamp']),
        ]
        # Prevent duplicate interactions of same type by same user on same pin
        unique_together = ['user', 'pin', 'interaction_type']
    
    def __str__(self):
        return f"{self.user.username} {self.interaction_type} {self.pin.title[:30]}"

class SearchQuery(models.Model):
    """User search queries"""
    query_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='search_queries')
    query_text = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)
    results_count = models.PositiveIntegerField(default=0)
    clicked_results = models.PositiveIntegerField(default=0)
    session_id = models.UUIDField(blank=True, null=True)
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['user', '-timestamp']),
            models.Index(fields=['query_text']),
        ]
    
    def __str__(self):
        return f"{self.user.username}: {self.query_text}"
    
    @property
    def click_through_rate(self):
        """Calculate click-through rate for search"""
        if self.results_count == 0:
            return 0
        return (self.clicked_results / self.results_count) * 100

# ML-specific models for recommendations

class UserProfile(models.Model):
    """User profile for ML recommendations"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    # Category preferences (computed from interactions)
    category_preferences = models.JSONField(default=dict)
    
    # Behavioral features
    avg_session_duration = models.FloatField(default=0.0)
    interaction_frequency = models.FloatField(default=0.0)
    preferred_pin_types = models.JSONField(default=list)
    
    # Temporal patterns
    active_hours = models.JSONField(default=list)  # Hours when user is most active
    active_days = models.JSONField(default=list)   # Days when user is most active
    
    last_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Profile for {self.user.username}"

class RecommendationLog(models.Model):
    """Log of recommendations shown to users"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pin = models.ForeignKey(Pin, on_delete=models.CASCADE)
    
    RECOMMENDATION_TYPES = [
        ('collaborative', 'Collaborative Filtering'),
        ('content_based', 'Content-Based'),
        ('trending', 'Trending'),
        ('hybrid', 'Hybrid'),
    ]
    
    recommendation_type = models.CharField(max_length=30, choices=RECOMMENDATION_TYPES)
    confidence_score = models.FloatField()
    position = models.PositiveIntegerField()  # Position in recommendation list
    
    shown_at = models.DateTimeField(auto_now_add=True)
    clicked = models.BooleanField(default=False)
    saved = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-shown_at']
        indexes = [
            models.Index(fields=['user', '-shown_at']),
            models.Index(fields=['recommendation_type']),
        ]
    
    def __str__(self):
        return f"Recommendation: {self.pin.title[:30]} to {self.user.username}"