from django import forms
from .models import Review


class RentalOrderForm(forms.Form):
    car_id = forms.IntegerField(widget=forms.HiddenInput())
    customer_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Customer name'}),
        label='Customer Name',
    )
    customer_email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email'}),
        label='Email address',
        help_text="We'll never share your email with anyone else.",
    )
    customer_mobile = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter mobile number'}),
        label='Mobile Number',
        help_text="We'll never share your mobile number with anyone else.",
    )
    customer_address = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Address'}),
        label='Address',
    )
    totalRentHour = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter The Number Of Hour You Want to Rent', 'id': 'id_totalRentHour'}),
        label='Total Hour You Want to Rent',
        min_value=1,
    )
    totalRentCar = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter The Number Of Car You Want to Rent', 'id': 'id_totalRentCar'}),
        label='Total Number of Car You Want to Rent',
        min_value=1,
    )
    include_driver = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'id_include_driver'}),
        label='Include Driver',
    )
    coupon_code = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter coupon code', 'id': 'id_coupon_code'}),
        label='Coupon Code',
    )
    deliveryDate = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        label='Delivery Date',
    )
    deliveryTime = forms.TimeField(
        widget=forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
        label='Delivery Time',
    )


class ReviewForm(forms.ModelForm):
    rating = forms.IntegerField(
        min_value=1,
        max_value=5,
        widget=forms.HiddenInput(attrs={'id': 'id_rating'}),
    )

    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Share your experience with this vehicle...',
            }),
        }


class SearchForm(forms.Form):
    search_key = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control me-2', 'placeholder': 'Search', 'aria-label': 'Search'}),
    )
