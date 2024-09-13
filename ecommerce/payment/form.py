from django import forms
from payment.models import ShippingAddress


class ShippingForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = [
            "full_name",
            "phone",
            "address1",
            "address2",
            "city",
            "state",
            "zip_code",
        ]
        exclude = ["user"]
        widgets = {
            "full_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Full Name",
                    "required": True,
                }
            ),
            "phone": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Phone Number",
                    "required": True,
                }
            ),
            "address1": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Address Line 1",
                    "required": True,
                }
            ),
            "address2": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Address Line 2",
                    "required": True,
                }
            ),
            "city": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "City",
                    "required": True,
                }
            ),
            "state": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "State"}
            ),
            "zip_code": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Zip Code"}
            ),
        }
