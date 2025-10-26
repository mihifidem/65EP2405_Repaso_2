from django.contrib import admin
from .models import ProfileUser, Categoria, SubCategoria, Hashtag, Post

@admin.register(Categoria, SubCategoria, Hashtag)
class TaxAdmin(admin.ModelAdmin):
    list_display = ("titulo","fecha_creacion")
    search_fields = ("titulo",)
    list_filter = ("fecha_creacion",)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("titulo","categoria","fecha_creacion")
    search_fields = ("titulo","_contenido")
    list_filter = ("categoria","fecha_creacion")

admin.site.register(ProfileUser)
