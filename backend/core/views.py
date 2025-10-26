from django.shortcuts import render, redirect
from django.core.exceptions import PermissionDenied
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Post, Categoria, Hashtag, SubCategoria
from .forms import PostForm
from .permissions import is_admin
from django.db.models import Q
from django.views.generic import ListView
from django.template.loader import render_to_string
from django.http import JsonResponse

from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import CategoriaForm, SubCategoriaForm, HashtagForm


# ✅ Crear categoría
@login_required
def crear_categoria(request):
    if not is_admin(request.user):
        raise PermissionDenied("Solo los administradores pueden crear categorías.")
    if request.method == "POST":
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Categoría creada con éxito.")
            return redirect("core:post_list")
    else:
        form = CategoriaForm()
    return render(request, "core/categoria_form.html", {"form": form})


# ✅ Crear subcategoría
@login_required
def crear_subcategoria(request):
    if not is_admin(request.user):
        raise PermissionDenied("Solo los administradores pueden crear subcategorías.")
    if request.method == "POST":
        form = SubCategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Subcategoría creada con éxito.")
            return redirect("core:post_list")
    else:
        form = SubCategoriaForm()
    return render(request, "core/subcategoria_form.html", {"form": form})


# ✅ Crear hashtag
@login_required
def crear_hashtag(request):
    if not is_admin(request.user):
        raise PermissionDenied("Solo los administradores pueden crear hashtags.")
    if request.method == "POST":
        form = HashtagForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Hashtag creado con éxito.")
            return redirect("core:post_list")
    else:
        form = HashtagForm()
    return render(request, "core/hashtag_form.html", {"form": form})


class PostListView(ListView):
    model = Post
    template_name = 'core/post_list.html'
    context_object_name = 'object_list'

    def get_queryset(self):
        queryset = Post.objects.all().select_related('categoria').prefetch_related('subcategorias')
        search = self.request.GET.get('search')
        categoria = self.request.GET.get('categoria')
        subcategoria = self.request.GET.get('subcategoria')
        orden = self.request.GET.get('orden')

        # ✅ Buscar en título, _contenido y _contenido_premium
        if search:
            queryset = queryset.filter(
                Q(titulo__icontains=search) |
                Q(_contenido__icontains=search) |
                Q(_contenido_premium__icontains=search)
            )

        if categoria:
            queryset = queryset.filter(categoria_id=categoria)

        if subcategoria:
            queryset = queryset.filter(subcategorias__id=subcategoria)

        if orden:
            queryset = queryset.order_by(orden)
        else:
            queryset = queryset.order_by('-fecha_creacion')

        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = Categoria.objects.all()
        context['subcategorias'] = SubCategoria.objects.all()
        return context

    def render_to_response(self, context, **response_kwargs):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            html = render_to_string('core/_post_list_partial.html', context, request=self.request)
            return JsonResponse({'html': html})
        return super().render_to_response(context, **response_kwargs)


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
    success_url = reverse_lazy("core:post_list")

    def form_valid(self, form):
        # Asigna el autor solo si existe el campo en el modelo
        if hasattr(form.instance, "autor"):
            form.instance.autor = self.request.user
        return super().form_valid(form)

class PostUpdateView(AdminRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "core/post_form.html"
    success_url = reverse_lazy("core:post_list")

class PostDeleteView(AdminRequiredMixin, DeleteView):
    model = Post
    template_name = "core/post_confirm_delete.html"
    success_url = reverse_lazy("core:post_list")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "🗑️ Post eliminado correctamente.")
        return super().delete(request, *args, **kwargs)

