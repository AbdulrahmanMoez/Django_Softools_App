from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from django.core.exceptions import ValidationError
from django.contrib import auth, messages

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(max_length=150, required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    password1 = forms.CharField(widget=forms.PasswordInput, max_length=128, required=True)
    password2 = forms.CharField(widget=forms.PasswordInput, max_length=128, required=True)
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("A user with that email already exists.")
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if ' ' in username:
            raise ValidationError("Username cannot contain spaces.")
        return username
        
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 != password2:
            raise ValidationError("Passwords do not match.")
        return password2
    
    # Save method sets the password and saves the user object if commit is True.
    # If commit is False, the user object is returned without saving it to the database.
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

class CustomUserLoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        
        errors = {}
        if not username:
            errors['username'] = 'Please enter your username'
        elif len(username) < 3:
            errors['username'] = 'Username must be at least 3 characters long'
            
        if not password:
            errors['password'] = 'Please enter your password'
        elif len(password) < 8:
            errors['password'] = 'Password must be at least 8 characters long'
            
        if errors:
            raise ValidationError(errors)
            
        return cleaned_data

    def validate_data(self, request):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        
        user = auth.authenticate(username=username, password=password)
        
        if not user:
            if User.objects.filter(username=username).exists():
                raise ValidationError("The password you entered is incorrect. Please try again.", code='invalid_password')
            raise ValidationError("No account found with this username. Please check your spelling or create an account.", code='invalid_username')
            
        if not user.is_active:
            raise ValidationError("Your account has been deactivated. Please contact support.", code='inactive')
        if user.is_staff:
            raise ValidationError("Please use the admin login page for staff accounts.", code='staff')
            
        auth.login(request, user)
        return self.cleaned_data

