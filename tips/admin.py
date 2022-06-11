from django.contrib import admin
from .models import Tip, TipTags, TipComment, Category


# Register your models here.



admin.site.register(Tip)
admin.site.register(Category)
admin.site.register(TipTags)
admin.site.register(TipComment)