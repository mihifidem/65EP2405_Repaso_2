from rest_framework import serializers
from .models import Post

class PostListSerializer(serializers.ModelSerializer):
    categoria = serializers.StringRelatedField()
    subcategorias = serializers.StringRelatedField(many=True)
    hashtags = serializers.StringRelatedField(many=True)
    class Meta:
        model = Post
        fields = ("id","titulo","categoria","subcategorias","hashtags","fecha_creacion")

class PostDetailSerializer(PostListSerializer):
    class Meta(PostListSerializer.Meta):
        fields = PostListSerializer.Meta.fields + ("contenido","contenido_premium",)
