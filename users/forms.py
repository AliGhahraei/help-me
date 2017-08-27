from django import forms
from django.contrib.auth.models import User


class RegisterForm(forms.ModelForm):
    username = forms.CharField(max_length=50)
    email = forms.EmailField(max_length=252)
    password = forms.CharField(widget=forms.PasswordInput)
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
