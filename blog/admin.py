from django.contrib import admin
from .models import Blog, BlogTags, BlogComment, Category
from mptt.admin import MPTTModelAdmin, DraggableMPTTAdmin


# Register your models here.

class CommentsAdmin(DraggableMPTTAdmin):
    list_display=(
        'tree_actions',
        'indented_title',)

admin.site.register(Blog)
admin.site.register(Category)
admin.site.register(BlogTags)
admin.site.register(BlogComment, DraggableMPTTAdmin)