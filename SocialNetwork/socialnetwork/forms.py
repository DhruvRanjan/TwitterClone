from django import forms
from django.contrib.auth.models import User
from socialnetwork.models import myUser

class RegistrationForm(forms.Form):

    username = forms.CharField(max_length = 20)
    password = forms.CharField(max_length = 200,
                               label = 'Password',
                               widget = forms.PasswordInput())
    passwordRepeat = forms.CharField(max_length = 200,
                                     label = 'Confirm password',
                                     widget = forms.PasswordInput())
    first_name = forms.CharField(max_length = 20)
    last_name = forms.CharField(max_length = 20)

    def clean(self):

        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        passwordRepeat = cleaned_data.get('passwordRepeat')
        if password != passwordRepeat:
            raise forms.ValidationError("Passwords are not the same")

        return cleaned_data

    def clean_username(self):

        username = self.cleaned_data.get('username')
        return username

#class FollowForm(forms.Form):

    

class editProfileForm(forms.Form):

    first_name = forms.CharField(max_length = 20, required=False)
    last_name = forms.CharField(max_length = 20, required=False)
    age = forms.IntegerField(required=False)
    bio = forms.CharField(max_length=430, required=False)
    profile_picture = forms.ImageField(label='Select file', required=False)

    class Meta:
        model = myUser
        exclude = ('ip_addr', 'content_type')
    
    def clean_picture(self):

        picture = self.cleaned_data['profile_picture']
        if not picture:
            return None
        if not picture.content_type or not picture.content_type.startswith('image'):
            raise forms.ValidationError('File is not an image')
        if picture.size > 25000000:
            raise forms.ValidationError('File too big. Maximum size is {0} bytes.')
        print "picture accepted"
        return picture

    def clean(self):

        cleaned_data = super(editProfileForm, self).clean()
        return cleaned_data

class PostForm(forms.Form):

    post_text = forms.CharField(max_length = 160)
    
    def clean(self):

        cleaned_data = super(PostForm, self).clean()
        return cleaned_data

class CommentForm(forms.Form):

    comment_text = forms.CharField(max_length=160)

    def clean(self):

        cleaned_data = super(PostForm, self).clean()
        return cleaned_data
