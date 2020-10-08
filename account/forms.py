from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpView(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'password1',
            'password2',
        ]
