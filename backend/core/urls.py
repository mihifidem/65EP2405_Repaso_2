from . import views
from django.urls import path
from .views import post_list, PostListView,PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, crear_categoria, crear_subcategoria, crear_hashtag
app_name = "core"

urlpatterns = [
    path("", PostListView.as_view(), name="post_list"),
    path("post/<int:pk>/", PostDetailView.as_view(), name="post_detail"),
    path("post/new/", PostCreateView.as_view(), name="post_create"),
    path("post/<int:pk>/edit/", PostUpdateView.as_view(), name="post_edit"),
    path("post/<int:pk>/delete/", PostDeleteView.as_view(), name="post_delete"),
    # Categorías / Subcategorías / Hashtags (solo admin)
    path("categoria/new/", crear_categoria, name="categoria_create"),
    path("subcategoria/new/", crear_subcategoria, name="subcategoria_create"),
    path("hashtag/new/", crear_hashtag, name="hashtag_create"),
    
    # AJAX — gestión de hashtags
    path('ajax/check_or_create_hashtag/', views.check_or_create_hashtag, name='check_or_create_hashtag'),
    path('ajax/delete_hashtag/<int:hashtag_id>/', views.delete_hashtag, name='delete_hashtag'),
    path('ajax/remove_hashtag/<int:post_id>/<int:hashtag_id>/', views.remove_hashtag_from_post, name='remove_hashtag_from_post'),


]