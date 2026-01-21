from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Cuenta

@receiver(post_save, sender=Cuenta)
def crear_usuario(sender, instance, created, **kwargs):
    if created:
        if not instance.user:
            username = instance.persona.correo
            password = User.objects.make_random_password()

            user = User.objects.create_user(
                username=username,
                email=instance.persona.correo,
                password=password
            )

            instance.user = user
            instance.save()
