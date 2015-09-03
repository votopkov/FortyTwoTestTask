from django import forms
from models import Profile


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, min_length=3,
                               label=u"",
                               widget=forms.TextInput(
                                   attrs={'placeholder': 'Login',
                                          'required': 'required'}))
    password = forms.CharField(label=u"",
                               widget=forms.TextInput(
                                   attrs={'placeholder': 'Password',
                                          'required': 'required',
                                          'type': 'password'}))


class ProfileForm(forms.ModelForm):
    id = forms.IntegerField(widget=forms.HiddenInput())
    name = forms.CharField(max_length=100,
                           min_length=3,
                           widget=forms.TextInput(
                               attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=100,
                                min_length=3,
                                widget=forms.TextInput(
                                    attrs={'class': 'form-control'}))
    date_of_birth = forms.CharField(max_length=100,
                                    min_length=3,
                                    widget=forms.TextInput(
                                        attrs={'class':
                                               'form-control datepicker'}))
    photo = forms.ImageField(required=False,
                             widget=forms.FileInput)
    email = forms.EmailField(max_length=100,
                             min_length=3,
                             widget=forms.TextInput(attrs={'class':
                                                           'form-control'}))
    jabber = forms.CharField(max_length=100,
                             min_length=3,
                             widget=forms.TextInput(attrs={'class':
                                                           'form-control'}))
    skype = forms.CharField(max_length=100,
                            min_length=3,
                            widget=forms.TextInput(attrs={'class':
                                                          'form-control'}))
    other_contacts = forms.CharField(max_length=1000,
                                     widget=forms.Textarea(
                                         attrs={'class':
                                                'form-control'}))
    bio = forms.CharField(max_length=1000,
                          widget=forms.Textarea(
                              attrs={'class': 'form-control'}))

    class Meta:
        model = Profile
        fields = ['id', 'name', 'last_name',
                  'date_of_birth', 'photo', 'bio',
                  'email', 'jabber', 'skype',
                  'other_contacts']
