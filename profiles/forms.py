from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from .models import Profile

class EditProfileForm(UserChangeForm):
    password = None  # Hide password field from form

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username']

class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput, label="Old Password")
    new_password = forms.CharField(widget=forms.PasswordInput, label="New Password")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm New Password")

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")
        if new_password and confirm_password and new_password != confirm_password:
            raise forms.ValidationError("New passwords do not match.")
        return cleaned_data

class ProfileImageForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_image']




#from django import forms
#from django.contrib.auth.models import User
#from .models import Profile

#class EditProfileForm(forms.ModelForm):
#    class Meta:
 #       model = User
#      fields = ['first_name', 'last_name', 'username', 'password']
 #       widgets = {
  #          'password': forms.PasswordInput(),
   #     }

#class ProfileImageForm(forms.ModelForm):
#    class Meta:
 #      fields = ['profile_image']
