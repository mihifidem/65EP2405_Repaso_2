from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .api_views import PostListCreateAPI, PostRetrieveAPI

urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("posts/", PostListCreateAPI.as_view(), name="api_posts"),
    path("posts/<int:pk>/", PostRetrieveAPI.as_view(), name="api_post_detail"),
]
