from django.db import models
from taggit.managers import TaggableManager
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    slug = models.SlugField(max_length=100, unique=True)

    def save(self, *args, **kwargs):
        self.slug = self.name.lower().replace(' ', '-')
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class Video(models.Model):
    title = models.CharField(max_length=100)
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    file = models.FileField(upload_to='videos/%Y/%m/%d', blank=True, null=True)
    youtube_link = models.URLField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
