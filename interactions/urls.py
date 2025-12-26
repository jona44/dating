from django.urls import path
from .views import like_user_view, skip_user_view

urlpatterns = [
    path("like/<uuid:user_id>/", like_user_view, name="like_user"),
    path("skip/<uuid:user_id>/", skip_user_view, name="skip_user"),
]
