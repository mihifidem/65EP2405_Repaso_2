from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import ProfileUser, Category, Subcategory, Hashtag, Post
from faker import Faker
import random

class Command(BaseCommand):
    help = "Genera datos de ejemplo para Blog (usuarios, categorías, posts)."

    def handle(self, *args, **options):
        fake = Faker("es_ES")

        # Usuarios + perfiles
        users = [("admin","admin123","admin"),("user","user123","user"),("premium","premium123","premium")]
        for u, p, r in users:
            usr, created = User.objects.get_or_create(username=u)
            if created:
                usr.set_password(p); usr.save()
            ProfileUser.objects.get_or_create(user=usr, defaults={"role": r})

        # Taxonomía
        categorias = [Category.objects.create(titulo=fake.word()) for _ in range(3)]
        subcats = [Subcategory.objects.create(titulo=fake.word()) for _ in range(4)]
        tags = [Hashtag.objects.create(titulo=fake.word()) for _ in range(6)]

        # Posts
        admin = User.objects.get(username="admin")
        for _ in range(10):
            post = Post.objects.create(
                titulo=fake.sentence(nb_words=5),
                categoria=random.choice(categorias),
                autor=admin,
                _contenido=fake.paragraph(nb_sentences=4),
                _contenido_premium=fake.text(180),
            )
            post.subcategorias.set(random.sample(subcats, k=2))
            post.hashtags.set(random.sample(tags, k=3))
            post.save()

        self.stdout.write(self.style.SUCCESS("Datos de ejemplo creados ✅"))
