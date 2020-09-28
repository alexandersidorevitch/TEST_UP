from django import forms

from home.models import Users


class UserForm(forms.ModelForm):
    class Meta:
        model = Users
        exclude = ['session']
