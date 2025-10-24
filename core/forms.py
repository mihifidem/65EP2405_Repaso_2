from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    # Campos del formulario que se conectan a las propiedades
    contenido = forms.CharField(widget=forms.Textarea)
    contenido_premium = forms.CharField(
        widget=forms.Textarea, required=False, label="Contenido Premium"
    )

    class Meta:
        model = Post
        fields = ("titulo", "categoria", "subcategorias", "hashtags", "contenido", "contenido_premium")

    def save(self, commit=True):
        """Sobrescribimos save() para usar las propiedades."""
        instance = super().save(commit=False)
        instance.contenido = self.cleaned_data.get("contenido")
        instance.contenido_premium = self.cleaned_data.get("contenido_premium")
        if commit:
            instance.save()
            self.save_m2m()
        return instance
