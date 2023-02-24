from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from PIL import Image # PIL, bibliothèque pour redimensionner les photos.
# Create your models here.
class Ticket(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField(max_length=2048, blank=True)
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True)
    time_created = models.DateField(auto_now_add=True) #, auto_now=False, default=django.utils.timezone.now())

    IMAGE_MAX_SIZE = (400, 400) # valeur et largeur de pixel dans une constante de class
    def resize_image(self): # Methode dans le modèle où se trouve la photo
        image = Image.open(self.image)
        image.thumbnail(self.IMAGE_MAX_SIZE) # thumbnail est la méthode qui permet de redimmensionner l'image
        # argumeents est largeur et hauteur en pixel max
        image.save(self.image.path) # sauvegarder en appelant la méthode save et en passant en argument
        # le chemin de l'image

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            self.resize_image()

class Review(models.Model):
    ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    headline = models.CharField(max_length=128)
    body = models.TextField(max_length=8192, blank=True, verbose_name="Commentaire")
    time_created = models.DateField(auto_now_add=True)

class UserFollows(models.Model):
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='following')
    followed_user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='followed_by')

    class Meta:
        unique_together = ('user', 'followed_user')




