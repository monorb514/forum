from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm
from forum.models import Profile


User = get_user_model()


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "full_name", "username", "password1", "password2")


class EditUserProfileForm(UserChangeForm):
    class Meta:
        model = Profile
        fields = ['bio', 'image']



