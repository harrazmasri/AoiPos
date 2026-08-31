import re
from django import forms
from aoiPosApp.models import User


class RegisterForm (forms.ModelForm):
    r_password = forms.CharField(
        widget = forms.PasswordInput(),
        label = "Repeat Password",
        required = True
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

        if email and not re.fullmatch(email_pattern, email):
            raise forms.ValidationError("Email must be of example@email.com")

        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        r_password = cleaned_data.get('r_password')

        if password and r_password and password != r_password:
            # Explicitly attach the error to r_password
            self.add_error('r_password', 'Password mismatch')

        return cleaned_data

class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'example@email.com'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput()
    )

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if email and password:
            try:
                user = User.objects.get(email=email)

                if user.password != password:
                    self.add_error(None, "Invalid email or password")
                else:
                    self.user_cache = user

            except User.DoesNotExist:
                self.add_error(None, "Invalid email or password")

        return cleaned_data