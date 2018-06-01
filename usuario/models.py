from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.conf import settings
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.created(user=instance)

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/capa/{1}'.format(instance.user.id, filename)

class Perfil(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    capa = models.ImageField(upload_to=user_directory_path, blank=True)
    dn = models.DateField(null=True, blank=True)
    sobre = models.TextField(blank=True)
    cidade = models.CharField(max_length=250, blank=True)
    def get_absolute_url(self):
        return reverse('perfil', kwargs={'pk': self.pk})



@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        perfil = Perfil(user=instance)
        perfil.capa = 'profile_image/defaut.jpeg'
        perfil.save()

