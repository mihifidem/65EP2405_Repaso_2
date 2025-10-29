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

]