from django import forms
from django.contrib.auth.models import User
from .models import memberBasic, memberPhoneNumber, memberWebsite, websiteType


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
    )


class SignUpForm(forms.Form):
    firstName = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
    )
    lastName = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
    )
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
    )
    password = forms.CharField(
        min_length=8,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
    )
    retypePassword = forms.CharField(
        min_length=8,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}),
    )

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('This username is taken before.')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is already in use.')
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        retypePassword = cleaned_data.get('retypePassword')
        if password and retypePassword and password != retypePassword:
            raise forms.ValidationError("Re-entered password doesn't match.")
        return cleaned_data


class VerificationForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control mt-2', 'placeholder': 'Email'}),
    )
    token = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Verification Code'}),
    )


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = memberBasic
        fields = ['firstName', 'lastName', 'memberDivision', 'memberDistrict', 'memberBirthDate', 'about']
        widgets = {
            'firstName': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'lastName': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'memberDivision': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Division'}),
            'memberDistrict': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'District'}),
            'memberBirthDate': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'about': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'cols': 50}),
        }


class PhoneNumberForm(forms.ModelForm):
    class Meta:
        model = memberPhoneNumber
        fields = ['phoneNumber']
        widgets = {
            'phoneNumber': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
        }


class WebsiteForm(forms.ModelForm):
    class Meta:
        model = memberWebsite
        fields = ['address', 'type']
        widgets = {
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
        }
