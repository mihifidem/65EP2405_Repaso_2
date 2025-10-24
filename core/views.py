from django.shortcuts import render
from django.core.exceptions import PermissionDenied
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Post, Categoria
from .forms import PostForm
from .permissions import is_admin

# FBV: listado público (anónimo ve títulos)
def post_list(request):
    posts = Post.objects.select_related("categoria").all().order_by("-fecha_creacion")
    return render(request, "core/post_list.html", {"posts": posts, "categorias": Categoria.objects.all()})

# Detalle: requiere login (user/premium/admin)
class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = "core/post_detail.html"

# Solo admin puede crear/editar/borrar
class AdminRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not is_admin(request.user):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

class PostCreateView(AdminRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "core/post_form.html"
    success_url = reverse_lazy("post_list")
    def form_valid(self, form):
        form.instance.autor = self.request.user
        return super().form_valid(form)

class PostUpdateView(AdminRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "core/post_form.html"
    success_url = reverse_lazy("post_list")

class PostDeleteView(AdminRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy("post_list")

