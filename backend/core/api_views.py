from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Post
from .serializers import PostListSerializer, PostDetailSerializer

class PostListCreateAPI(generics.ListCreateAPIView):
    queryset = Post.objects.select_related("categoria").all().order_by("-fecha_creacion")
    serializer_class = PostListSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = {"categoria":["exact"]}
    search_fields = ["titulo","categoria__titulo"]
    ordering_fields = ["fecha_creacion","titulo"]

    def get_permissions(self):
        if self.request.method == "POST":
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        user = self.request.user
        role = getattr(getattr(user,"profile",None),"role",None)
        if role != "admin":
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("Solo admin puede crear posts.")
        serializer.save(autor=user)

class PostRetrieveAPI(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    def get_serializer_class(self):
        if self.request.user.is_authenticated:
            return PostDetailSerializer
        return PostListSerializer
