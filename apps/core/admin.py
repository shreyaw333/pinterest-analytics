from django.contrib import admin
from .models import User, Board, Pin, UserInteraction, SearchQuery, UserProfile, RecommendationLog

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'account_type', 'followers_count', 'pins_count', 'is_verified']
    list_filter = ['account_type', 'is_verified', 'created_at']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    readonly_fields = ['user_id', 'created_at', 'last_active']

@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'category', 'subcategory', 'pins_count', 'is_private']
    list_filter = ['category', 'is_private', 'created_at']
    search_fields = ['title', 'user__username']
    readonly_fields = ['board_id', 'created_at', 'updated_at']

@admin.register(Pin)
class PinAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'category', 'saves_count', 'trending_score', 'created_at']
    list_filter = ['category', 'is_promoted', 'created_at']
    search_fields = ['title', 'user__username']
    readonly_fields = ['pin_id', 'created_at', 'updated_at', 'engagement_rate']
    ordering = ['-trending_score']

@admin.register(UserInteraction)
class UserInteractionAdmin(admin.ModelAdmin):
    list_display = ['user', 'pin', 'interaction_type', 'device_type', 'timestamp']
    list_filter = ['interaction_type', 'device_type', 'referrer', 'timestamp']
    search_fields = ['user__username', 'pin__title']
    readonly_fields = ['interaction_id', 'timestamp']

@admin.register(SearchQuery)
class SearchQueryAdmin(admin.ModelAdmin):
    list_display = ['user', 'query_text', 'results_count', 'clicked_results', 'timestamp']
    list_filter = ['timestamp']
    search_fields = ['user__username', 'query_text']
    readonly_fields = ['query_id', 'timestamp', 'click_through_rate']

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'interaction_frequency', 'last_updated']
    search_fields = ['user__username']
    readonly_fields = ['last_updated']

@admin.register(RecommendationLog)
class RecommendationLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'pin', 'recommendation_type', 'confidence_score', 'position', 'clicked', 'saved']
    list_filter = ['recommendation_type', 'clicked', 'saved', 'shown_at']
    search_fields = ['user__username', 'pin__title']
    readonly_fields = ['shown_at']