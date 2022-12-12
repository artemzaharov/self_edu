from django.db import models
from django.urls import reverse
# Create your models here.


class Women(models.Model):
    # id is automaticly added in .Model
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    # we need MEDIA_ROOT, MEDIA_URL to use media files in development
    photo = models.ImageField(upload_to="photos/%Y/%m/%d")
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, null=True)
    # to check what sql command we run in term ./manage.py sqlmigrate women 0001
    # file 0001_initial.py was created after makemigrations

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post", kwargs={"post_id": self.pk})


class Category(models.Model):

    name = models.CharField(max_length=180, db_index=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("category", kwargs={"cat_id": self.pk})
