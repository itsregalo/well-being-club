from django.db import models
import uuid

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

class Content(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField('Tag')
    language =models.CharField(max_length=100, blank=True, null=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)

    def __str__(self):
        return self.title

class ContentFile(models.Model):
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    file = models.FileField()
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)

    def __str__(self):
        return self.file.name