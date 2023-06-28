from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms

class CreateUserForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control mb-3"}), required=True,
        label="User Name",
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"class": "form-control mb-3"}), required=True,
        label="Email Address",
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control mb-3"}), required=True,
        label="Password"
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control mb-3"}), required=True,
        label="Password Confirmation",
    )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        self.fields["username"].help_text = None
        self.fields["username"].widget.attrs.update({"placeholder": "User Name"})
        self.fields["email"].help_text = None
        self.fields["email"].widget.attrs.update({"placeholder": "Email Address"})
        self.fields["password1"].help_text = None
        self.fields["password1"].widget.attrs.update({"placeholder": "Password"})
        self.fields["password2"].help_text = None
        self.fields["password2"].widget.attrs.update(
            {"placeholder": "Password Confirmation"}
        )

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if len(username) >= 250:
            raise forms.ValidationError("the username is too long")
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("the email is already exists")
        if len(email) >= 250:
            raise forms.ValidationError("the email is too long")
        return email

    # def clean_password2(self):
    #     password1 = self.cleaned_data.get("password1")
    #     password2 = self.cleaned_data.get("password2")
    #     if len(password1) >= 250:
    #         raise forms.ValidationError("the password is too long")
    #     if password1 != password2:
    #         raise forms.ValidationError("the password is not match")
    #     return password2

    # def clean_password1(self):
    #     password = self.cleaned_data.get("password1")
    #     if len(password) >= 250:
    #         raise forms.ValidationError("the password is too long")

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control mb-3"}), required=True)
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control mb-3"}), required=True)
    

class UpdateUserForm(forms.ModelForm):
    password = None
    username = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control mb-3"}), required=True,
        label="User Name",
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"class": "form-control mb-3"}), required=True,
        label="Email Address",
    )
    class Meta:
        model = User
        fields = ["username", "email"]
        exclude = ["password1", "password2"]

    def __init__(self, *args, **kwargs):
        super(UpdateUserForm, self).__init__(*args, **kwargs)
        self.fields["username"].help_text = None
        self.fields["username"].widget.attrs.update({"placeholder": "User Name"})
        self.fields["email"].help_text = None
        self.fields["email"].required = True
        self.fields["email"].widget.attrs.update({"placeholder": "Email Address"})

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if len(username) >= 250:
            raise forms.ValidationError("the username is too long")
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exclude(id=self.instance.id).exists():
            raise forms.ValidationError("the email is already exists")
        if len(email) >= 250:
            raise forms.ValidationError("the email is too long")
        return email