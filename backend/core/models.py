from django.db import models
from django.contrib.auth.models import User


# ============================================================
# Clase base abstracta — Abstracción
# ============================================================
# Esta clase define atributos comunes para las entidades del blog.
# No crea tabla propia (abstract = True).
class BaseEntidad(models.Model):
    titulo = models.CharField(max_length=255)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True  # Django no crea tabla en la BD
        ordering = ["-fecha_creacion"]

    def __str__(self):
        return self.titulo


# ============================================================
# 👤 Perfil de usuario — Herencia 1 a 1 con User
# ============================================================
class ProfileUser(models.Model):
    ROLES = [
        ("user", "Usuario"),
        ("premium", "Premium"),
        ("admin", "Administrador"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLES, default="user")

    def __str__(self):
        return f"{self.user.username} ({self.role})"


# ============================================================
# 📚 Categoría principal (1 - N con Post)
# ============================================================
class Categoria(BaseEntidad):
    descripcion = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Categorías"


# ============================================================
# 🏷️ Subcategoría (N - M con Post)
# ============================================================
class SubCategoria(BaseEntidad):
    # 🔗 Relación 1-N: una categoría puede tener muchas subcategorías
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.CASCADE,
        related_name="subcategorias"
    )

    class Meta:
        verbose_name_plural = "Subcategorías"

    def __str__(self):
        return f"{self.titulo} ({self.categoria.titulo})"



# ============================================================
# 🔖 Hashtag (N - M con Post)
# ============================================================
class Hashtag(BaseEntidad):
    class Meta:
        verbose_name_plural = "Hashtags"


# ============================================================
# 📝 Post — Modelo principal del blog
# ============================================================
# Aplica herencia, encapsulamiento y polimorfismo.
class Post(BaseEntidad):
    categoria = models.ForeignKey(
        Categoria, on_delete=models.CASCADE, related_name="posts"
    )
    subcategorias = models.ManyToManyField(
        SubCategoria, blank=True, related_name="posts"
    )
    hashtags = models.ManyToManyField(Hashtag, blank=True, related_name="posts")
    imagen = models.ImageField(upload_to='posts/', blank=True, null=True)  # 👈 NUEVO CAMPO


    # 🔒 Encapsulamiento: atributos protegidos
    _contenido = models.TextField()
    _contenido_premium = models.TextField(blank=True, null=True)

    # 👁️ Propiedades públicas (getters/setters)
    @property
    def contenido(self):
        """Obtiene el contenido público."""
        return self._contenido

    @contenido.setter
    def contenido(self, value):
        """Actualiza el contenido público."""
        self._contenido = value

    @property
    def contenido_premium(self):
        """Obtiene el contenido premium."""
        return self._contenido_premium

    @contenido_premium.setter
    def contenido_premium(self, value):
        """Actualiza el contenido premium."""
        self._contenido_premium = value

    # 💡 Polimorfismo: comportamiento adaptable
    def mostrar_info(self, modo="resumen"):
        """Devuelve información distinta según el modo solicitado."""
        if modo == "resumen":
            return f"{self.titulo} — {self.categoria.titulo}"
        elif modo == "detallado":
            return f"{self.titulo}\n{self.contenido[:120]}..."
        else:
            return str(self)

    class Meta:
        verbose_name_plural = "Posts"
