from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import (
    register_user, logout_user, current_user,
    ProfileViewSet, ProfilePhotoViewSet, PreferenceViewSet,
    LikeViewSet, MatchViewSet, BlockViewSet, ReportViewSet, SkipViewSet,
    ConversationViewSet, MessageViewSet
)

# Create router for ViewSets
router = DefaultRouter()
router.register(r'profiles', ProfileViewSet, basename='profile')
router.register(r'profile-photos', ProfilePhotoViewSet, basename='profile-photo')
router.register(r'preferences', PreferenceViewSet, basename='preference')
router.register(r'likes', LikeViewSet, basename='like')
router.register(r'matches', MatchViewSet, basename='match')
router.register(r'blocks', BlockViewSet, basename='block')
router.register(r'reports', ReportViewSet, basename='report')
router.register(r'skips', SkipViewSet, basename='skip')
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='message')

urlpatterns = [
    # Authentication
    path('auth/register/', register_user, name='register'),
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/logout/', logout_user, name='logout'),
    path('auth/me/', current_user, name='current-user'),
    
    # ViewSet routes
    path('', include(router.urls)),
]
