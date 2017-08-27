from django import forms
from django.contrib.auth.models import User
from users.models import Service, Comment


class RegisterForm(forms.ModelForm):
    password2 = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")

        if password != password2:
            raise forms.ValidationError("Passwords don't match")

        return cleaned_data

    class Meta:
        model = User
        fields = ['email', 'password', 'username']


class ServiceForm(forms.ModelForm):

    class Meta:
        model = Service
        fields = ['name', 'description', 'tags']


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['content']
