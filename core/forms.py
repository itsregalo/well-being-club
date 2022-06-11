from django import forms
from .models import Contact, EmailSubscriber

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'subject', 'message']

        widgets = {
            'name': forms.TextInput(attrs={"class":"contact-name form-control", "id":"name", "type":"text", "placeholder":"First Name"}),
            'email': forms.TextInput(attrs={"class":"contact-email form-control", "id":"L_name", "type":"email", "placeholder":"Your Email"}),
            'subject': forms.TextInput(attrs={"class":"contact-name form-control", "id":"L_name", "type":"text", "placeholder":"Subject"}),
            'message': forms.Textarea(attrs={"class":"form-control", "id":"message", "rows":"6", "placeholder":"Your Message"}),
        }


class EmailSubscriberForm(forms.ModelForm):
    class Meta:
        model = EmailSubscriber
        fields = ['email', 'receive_email']

        widgets = {
            'email': forms.TextInput(attrs={"class":"form-control","placeholder":"Enter Your Email"}),
            'receive_email': forms.CheckboxInput(attrs={"class":"custom-control-input", 
                                                        "type":"checkbox", 'id':'condition'}),
        }