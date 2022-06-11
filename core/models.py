from django.db import models

# Create your models here.

class Contact(models.Model):
    name = models.CharField(max_length=100)
    subject = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(max_length=100)
    message = models.TextField()

    def __str__(self):
        return self.name

class EmailSubscriber(models.Model):
    email = models.EmailField(max_length=100, unique=True)

    def __str__(self):
        return self.email