from django import forms
from .models import *
from django.contrib.auth.forms import  UserCreationForm, UserChangeForm
from django.contrib.auth.models import User


class NewPost(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['image', 'description', 'category', 'title']


        widgets = {
            'summary': forms.Textarea(attrs={
                'class': 'description',
                'rows': '4',
            })
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].widget.attrs.update({'id': 'postImage'})



class SignupForm(UserCreationForm):
    user_img = forms.ImageField()

    class Meta:
        model = User
        fields = ['user_img', 'username', 'first_name', 'last_name', 'email', 'password1', 'password2']
      

class UpdateProfileForm(UserChangeForm):
    profile_img = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['profile_img', 'username', 'first_name', 'last_name', 'email',]


class LoginForm(forms.Form):
    username = forms.CharField(required=True, widget=forms.TextInput(
        attrs={
        'placeholder': 'Username',
        'class': 'mb-2 border border-rounded border-primary',
        }
    ))
    password = forms.CharField(required=True, widget=forms.PasswordInput(
        attrs={
        'placeholder': 'Password',
        'class': 'mt-2 border border-rounded border-primary',
        }
    ))
    