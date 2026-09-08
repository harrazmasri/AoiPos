import re
from django import forms
from django.contrib.auth.hashers import check_password, make_password
from aoiPosApp.models import Product, Transaction, User
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password, check_password

def validate_file_size (file):
    max_mb = 5

    if file.size > max_mb * 1024 * 1024:
        raise ValidationError(f"File size must be less than { max_mb }MB.")

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

    def save(self, commit=True):
        user = super().save(commit=False)
        user.password = make_password(user.password)

        if commit:
            user.save()

        return user


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

                if not check_password(password, user.password):
                    self.add_error(None, "Invalid email or password")
                else:
                    self.user_cache = user

            except User.DoesNotExist:
                self.add_error(None, "Invalid email or password")

        return cleaned_data


class ProductForm(forms.ModelForm):

    image_path = forms.ImageField(
        required=False,
        validators=[
            FileExtensionValidator(
                allowed_extensions=['jpg', 'jpeg', 'png', 'webp']
            ),
            validate_file_size,
        ],
        widget=forms.FileInput(attrs={
            'accept': 'image/*'
        })
    )

    class Meta:
        model = Product
        fields = ['name', 'price', 'image_path']

    def clean_price(self):
        price = self.cleaned_data.get('price')
        
        if price is not None:
            return round(price, 2)
            
        return price



class TransactionForm(forms.ModelForm):
    class Meta:
        model=Transaction
        fields='__all__'