from django.db import models


# Create your models here.

class Meme(models.Model):
    caption = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to='memes/')
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.caption