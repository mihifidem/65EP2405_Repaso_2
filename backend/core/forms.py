from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    """Formulario personalizado que maneja los campos del modelo Post
    incluyendo las propiedades `contenido` y `contenido_premium`."""

    contenido = forms.CharField(
        label="Contenido público",
        required=True,
        widget=forms.Textarea(attrs={
            "class": "form-control",
            "rows": 5,
            "placeholder": "Escribe el contenido público..."
        }),
    )

    contenido_premium = forms.CharField(
        label="Contenido Premium",
        required=False,
        widget=forms.Textarea(attrs={
            "class": "form-control",
            "rows": 5,
            "placeholder": "Escribe el contenido premium (solo visible a usuarios Premium o Admin)..."
        }),
    )

    class Meta:
        model = Post
        fields = ["titulo", "categoria", "subcategorias", "hashtags"]
        widgets = {
            "titulo": forms.TextInput(attrs={"class": "form-control"}),
            "categoria": forms.Select(attrs={"class": "form-select"}),
            "subcategorias": forms.SelectMultiple(attrs={"class": "form-select"}),
            "hashtags": forms.SelectMultiple(attrs={"class": "form-select"}),
        }

    def __init__(self, *args, **kwargs):
        """Precarga el contenido del modelo si existe (modo edición)."""
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields["contenido"].initial = getattr(self.instance, "contenido", "")
            self.fields["contenido_premium"].initial = getattr(self.instance, "contenido_premium", "")

    def save(self, commit=True):
        """Guarda los valores en los campos protegidos del modelo."""
        instance = super().save(commit=False)
        instance.contenido = self.cleaned_data.get("contenido", "")
        instance.contenido_premium = self.cleaned_data.get("contenido_premium", "")
        if commit:
            instance.save()
            self.save_m2m()
        return instance
