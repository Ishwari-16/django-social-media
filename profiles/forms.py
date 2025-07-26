from django import forms
from django.contrib.auth.models import User
from .models import Profile

class EditProfileForm(forms.ModelForm):
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput(), required=False)
    image = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'password')

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)
        if commit:
            user.save()
            if 'image' in self.files:
                profile, created = Profile.objects.get_or_create(user=user)
                profile.image = self.cleaned_data['image']
                profile.save()
        return user
