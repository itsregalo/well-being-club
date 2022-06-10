from django.db import models
from django.db.models.deletion import DO_NOTHING
from django.utils.text import slugify
from PIL import Image
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from django.urls import reverse
from ckeditor.fields import RichTextField

from mptt.models import MPTTModel, TreeForeignKey
from taggit.managers import TaggableManager


from django.contrib.auth import get_user_model
User = get_user_model()
# Create your models here.

class Category(models.Model):
    name=models.CharField(max_length=255)
    slug = models.SlugField(blank=True)
    view_count = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name='category'
        verbose_name_plural='categories'
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug=slugify(self.name)
        return super(Category, self).save(*args, **kwargs)
    
    def get_tag_tips(self):
        return Tip.objects.filter(category=self)
    
class TipTags(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(blank=True)

    class Meta:
        verbose_name='tip tag'
        verbose_name_plural='tip tags'
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug=slugify(self.name)
        return super(TipTags, self).save(*args, **kwargs)
    
    def get_tag_tips(self):
        return Tip.objects.filter(tag=self)
    
class Tip(models.Model):
    title = models.CharField(max_length=255)
    uploaded_by = models.ForeignKey(User, on_delete=DO_NOTHING)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    pic = models.ImageField(upload_to="images/tip/%Y/%m/%d")
    pic_thumbnail = ImageSpecField(source='pic',
                                   processors = [ResizeToFill(800,356)],
                                   format='JPEG',
                                   options = {'quality':100})
    pic_thumbnail_small = ImageSpecField(source='pic',
                                   processors = [ResizeToFill(415,275)],
                                   format='JPEG',
                                   options = {'quality':50})
    pic_thumbnail_latest = ImageSpecField(source='pic',
                                   processors = [ResizeToFill(400,245)],
                                   format='JPEG',
                                   options = {'quality':50})
    content = RichTextField()
    tags = TaggableManager()
    pub_date = models.DateTimeField(auto_now_add=True)
    view_count = models.IntegerField(default=0)
    slug = models.SlugField(blank=True)
    is_approved = models.BooleanField(default=False)

    class Meta:
        ordering = ['-pub_date']
        verbose_name='tip'
        verbose_name_plural='tips'
    
    def __str__(self):
        return f"{self.uploaded_by.username} - {self.title}"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)+"-"+str(self.pk)
        return super(Tip,self).save(*args, **kwargs)
    
    def get_tip_tags(self):
        return self.tags.all()

    def get_tip_comments(self):
        return TipComment.objects.filter(post=self)

    def get_absolute_url(self):
        return reverse("tip:tip-detail", kwargs={"slug":self.slug, "pk": self.pk})
    
    
class TipComment(MPTTModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Tip, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, 
                null=True, blank=True, related_name='children')
    is_approved = models.BooleanField(default=False)
    
    class MPTTMeta:
        order_insertion_by = ['timestamp']

    class Meta:
        verbose_name='tip comment'
        verbose_name_plural='tip comments'

    def __str__(self):
        return f"{self.post.title} - {self.content}"
    
    