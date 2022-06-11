from django import forms
from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .models import TipComment, Tip

from mptt.forms import TreeNodeChoiceField


class TipForm(forms.ModelForm):
    class Meta:
        content = forms.CharField(widget=CKEditorUploadingWidget())
        model = Tip
        exclude = ['uploaded_by','pub_date','view_count','slug','pic_thumbnail','view_count']

        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control'}),
            'category': forms.Select(attrs={'class':'form-control mb-2'}),
            'content': forms.TextInput(attrs={'class':'form-control'}),
            'tags': forms.TextInput(attrs={'class':'form-control'}),
            'pic': forms.FileInput(attrs={'class':'form-control'}),
        }

        

class CommentForm(forms.ModelForm):
    class Meta:
        model = TipComment
        exclude = ['user','pub_date','post']

        widgets = {
            'content': forms.TextInput(attrs={'class':'form-control form-control-custom style_2', 
                                            'placeholder':'Write a comment...', 
                                            'rows':'5', 'autocomplete':'off'}),
        }

