from django.contrib import admin
from .models import Tip, TipTags, TipComment, Category
from mptt.admin import MPTTModelAdmin, DraggableMPTTAdmin


# Register your models here.

class CommentsAdmin(DraggableMPTTAdmin):
    list_display=(
        'tree_actions',
        'indented_title',)

admin.site.register(Tip)
admin.site.register(Category)
admin.site.register(TipTags)
admin.site.register(TipComment, DraggableMPTTAdmin)