from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class CreateUserForm(UserCreationForm):
    phone = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control mb-3"}),
        required=True,
        label="Phone Number",
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"class": "form-control mb-3"}),
        required=True,
        label="Email Address",
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control mb-3"}),
        required=True,
        label="Password",
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control mb-3"}),
        required=True,
        label="Password Confirmation",
    )

    class Meta:
        model = User
        fields = ["phone", "email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        self.fields["phone"].help_text = None
        self.fields["phone"].widget.attrs.update({"placeholder": "Phone Number"})
        self.fields["email"].help_text = None
        self.fields["email"].widget.attrs.update({"placeholder": "Email Address"})
        self.fields["password1"].help_text = None
        self.fields["password1"].widget.attrs.update({"placeholder": "Password"})
        self.fields["password2"].help_text = None
        self.fields["password2"].widget.attrs.update(
            {"placeholder": "Password Confirmation"}
        )

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        if User.objects.filter(phone=phone).exists():
            raise forms.ValidationError("The phone number already exists")
        return phone

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("The email already exists")
        return email


class LoginForm(AuthenticationForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control mb-3"}),
        required=True,
        label="Password",
    )

    class Meta:
        fields = ["password"]


class UpdateUserForm(forms.ModelForm):
    password = None
    phone = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control mb-3"}),
        required=True,
        label="Phone Number",
    )
    profile_image = forms.ImageField(
        required=False,
        widget=forms.FileInput(
            attrs={"class": "form-control mb-3"}, 
        ),
        label="Profile Image"
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"class": "form-control mb-3"}),
        required=True,
        label="Email Address",
    )

    class Meta:
        model = User
        fields = ["phone", "email", "first_name", "last_name", "profile_image"]

    def __init__(self, *args, **kwargs):
        super(UpdateUserForm, self).__init__(*args, **kwargs)
        self.fields["phone"].help_text = None
        self.fields["phone"].widget.attrs.update({"placeholder": "Phone Number"})
        self.fields["email"].help_text = None
        self.fields["email"].widget.attrs.update({"placeholder": "Email Address"})

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        if User.objects.filter(phone=phone).exclude(id=self.instance.id).exists():
            raise forms.ValidationError("The phone number already exists")
        return phone

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exclude(id=self.instance.id).exists():
            raise forms.ValidationError("The email already exists")
        return email
