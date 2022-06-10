from django import forms
from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .models import Blog, BlogComment

from mptt.forms import TreeNodeChoiceField


class BlogForm(forms.ModelForm):
    class Meta:
        content = forms.CharField(widget=CKEditorUploadingWidget())
        model = Blog
        exclude = ['uploaded_by','pub_date','view_count','slug','pic_thumbnail','view_count']

        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control'}),
            'category': forms.Select(attrs={'class':'form-control mb-2'}),
            'content': forms.TextInput(attrs={'class':'form-control'}),
            'tags': forms.TextInput(attrs={'class':'form-control'}),
            'pic': forms.FileInput(attrs={'class':'form-control'}),
        }

        

class CommentForm(forms.ModelForm):
    parent = TreeNodeChoiceField(queryset=BlogComment.objects.all())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['parent'].required = False
        self.fields['parent'].widget.attrs.update(
            {'class':'d-none'}
        )    
    class Meta:
        model = BlogComment
        fields = ['parent','content']

        widgets = {
            'content':forms.Textarea(attrs={'id':'content','rows':'4','cols':'40',
                                    'placeholder':'Enter Your Comment', 'class':'form-control mb-2'})
        }

