from django.forms import ModelForm
from .models import *


class RegisterForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget.attrs.update({'type': 'password'})
        # Add the user settings as a hidden field
        self.fields['settings'] = self.fields['settings'].widget(attrs={'type': 'hidden'})

    def save(self, commit=True):
        user = super().save(commit=False)
        # Hash the password
        user.set_password(self.cleaned_data['password'])

        # Create a settings object for the user upon registration
        settings = Settings.objects.create(user=user, dark_mode=False)
        settings.save()

        # Save
        if commit:
            user.save()
        return user


class LoginForm(ModelForm):
    class Meta:
        model = User
        fields = ['email', 'password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget.attrs.update({'type': 'password'})
