from django import forms
from ckeditor.widgets import CKEditorWidget
from .models import Categoria, SubCategoria, Hashtag, Post


# ============================================================
# 🧩 FORMULARIO DE CATEGORÍA
# ============================================================
class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ["titulo", "descripcion"]
        widgets = {
            "titulo": forms.TextInput(attrs={"class": "form-control"}),
            "descripcion": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }


# ============================================================
# 🧩 FORMULARIO DE SUBCATEGORÍA
# ============================================================
class SubCategoriaForm(forms.ModelForm):
    class Meta:
        model = SubCategoria
        fields = ["titulo", "categoria"]
        widgets = {
            "titulo": forms.TextInput(attrs={"class": "form-control"}),
            "categoria": forms.Select(attrs={"class": "form-select"}),
        }


# ============================================================
# 🧩 FORMULARIO DE HASHTAG
# ============================================================
class HashtagForm(forms.ModelForm):
    class Meta:
        model = Hashtag
        fields = ["titulo"]
        widgets = {
            "titulo": forms.TextInput(attrs={"class": "form-control"}),
        }


# ============================================================
# 📝 FORMULARIO DE POST — con CKEditor activo
# ============================================================
class PostForm(forms.ModelForm):
    # Campos visibles con editor visual
    contenido = forms.CharField(
        widget=CKEditorWidget(),
        label="Contenido público"
    )
    contenido_premium = forms.CharField(
        widget=CKEditorWidget(),
        label="Contenido premium",
        required=False
    )

    class Meta:
        model = Post
        fields = [
            "titulo",
            "categoria",
            "subcategorias",
            "imagen",
            "contenido",
            "contenido_premium",
            "hashtags",
        ]
        widgets = {
            "titulo": forms.TextInput(attrs={"class": "form-control"}),
            "categoria": forms.Select(attrs={"class": "form-select"}),
            "subcategorias": forms.SelectMultiple(attrs={"class": "form-select"}),
            "imagen": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "hashtags": forms.SelectMultiple(attrs={"class": "form-select"}),
        }

    # ============================================================
    # 🔄 Sincroniza datos del formulario con el modelo Post
    # ============================================================
    def save(self, commit=True):
        instance = super().save(commit=False)
        # asigna los valores al modelo real
        instance._contenido = self.cleaned_data["contenido"]
        instance._contenido_premium = self.cleaned_data.get("contenido_premium", "")
        if commit:
            instance.save()
            self.save_m2m()
        return instance

    # ============================================================
    # 🧠 Inicializa los campos con los valores del modelo (modo edición)
    # ============================================================
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields["contenido"].initial = self.instance._contenido
            self.fields["contenido_premium"].initial = self.instance._contenido_premium
