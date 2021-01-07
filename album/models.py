from django.db import models
from django.db.models.signals import post_delete
from django.urls import reverse
from django.dispatch import receiver


class Category(models.Model):
    """ Categorias para clasificar las fotos """

    name = models.CharField(max_length=50, verbose_name="Nombre")
    template = models.ImageField(upload_to='templates/', verbose_name="Plantilla")
    description = models.CharField(max_length=1000, verbose_name="Descripción")
    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = "categoria"
        verbose_name_plural = "categorias"
    
    def __str__(self):
        return self.name  # <=====

class Photo(models.Model):
    """ Fotos del album """

    category = models.ForeignKey(Category, on_delete=models.CASCADE,null=True, blank=True, verbose_name="Categoria")
    photo = models.ImageField(upload_to='photos/', verbose_name="Foto")
    pub_date = models.DateField(auto_now_add=True)
    toptext = models.CharField(max_length=200, blank=True, verbose_name="Texto Superior")
    bottomtext = models.CharField(max_length=200, blank=True, verbose_name="Texto Inferior")
    othertext = models.CharField(max_length=200, null=True, blank=True, verbose_name="Texto adicional")
     
    class Meta:
        verbose_name = "foto"
        verbose_name_plural = "fotos"

    def __str__(self):
        return self.category.name  # <=====

    def __unicode__(self):
        return self.category

    def get_absolute_url(self):
        return reverse('photo-list')


@receiver(post_delete, sender=Photo)
def photo_delete(sender, instance, **kwargs):
    """ Borra los ficheros de las fotos que se eliminan. """
    instance.photo.delete(False)