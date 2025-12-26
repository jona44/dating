from django.urls import path
from . import views

urlpatterns = [
    path('discover/', views.discovery_feed, name='discovery_feed'),
    path('like/<uuid:profile_id>/', views.like_profile_view, name='like_profile'),
    path('skip/<uuid:profile_id>/', views.skip_profile_view, name='skip_profile'),
    path('profile/<uuid:profile_id>/', views.profile_view, name='profile_view'),
    path('block/<uuid:profile_id>/', views.block_user_view, name='block_user'),
    path('report/<uuid:profile_id>/', views.report_user_view, name='report_user'),
    path('inbox/', views.inbox, name='inbox'),
    path('conversation/<uuid:conversation_id>/', views.conversation_detail, name='conversation_detail'),
    path('conversation/<uuid:conversation_id>/send/', views.send_message_view, name='send_message'),
    path('conversation/<uuid:conversation_id>/typing/',views.typing_ping,name='typing_ping' ),
    path('conversation/<uuid:conversation_id>/typing/status/',views.typing_status,name='typing_status'),
    path('discover/preferences/', views.preferences_view, name='preferences'),
    path('discover/search/', views.search_view, name='search'),
    path('activity/', views.activity_view, name='activity'),
    path('settings/', views.settings_view, name='settings'),
    path('help/', views.help_view, name='help'),
    path('privacy-policy/', views.privacy_view, name='privacy_policy'),
    path('terms/', views.terms_view, name='terms'),
    path('data-deletion/', views.data_deletion_view, name='data_deletion'),
]
