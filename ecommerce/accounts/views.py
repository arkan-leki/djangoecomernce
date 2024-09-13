from django.shortcuts import redirect, render
from accounts.forms import CreateUserForm, LoginForm, UpdateUserForm

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from accounts.tokens import user_activation_token
from django.contrib.auth import get_user_model
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from payment.form import ShippingForm

from payment.models import ShippingAddress

User = get_user_model()


# Create your views here.
def register(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            #  email verification setup
            current_site = get_current_site(request)
            subject = "Activate Your Account"
            message = render_to_string(
                "accounts/registration/email-verification-message.html",
                {
                    "user": user,
                    "domain": current_site.domain,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": user_activation_token.make_token(user),
                },
            )

            user.email_user(subject=subject, message=message)

            messages.success(request, "Account created successfully")

            return redirect("email-verification-sent")
        messages.warning(request, "Account creation failed")

    return render(request, "accounts/registration/register.html", {"form": form})


def email_verification(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and user_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Account activated successfully")
        return redirect("email-verification-success")
    else:
        messages.warning(request, "Account activation failed")
        return redirect("email-verification-failed")
    # return render(request, "accounts/registration/email_verification-message.html")


def email_verification_sent(request):
    return render(request, "accounts/registration/email-verification-sent.html")


def email_verification_success(request):
    return render(request, "accounts/registration/email-verification-success.html")


def email_verification_failed(request):
    return render(request, "accounts/registration/email-verification-failed.html")


def user_login(request):
    form = LoginForm(request)
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            phone = request.POST.get("username", "")
            password = request.POST.get("password", "")
            user = authenticate(request, phone=phone, password=password)
            print(user)
            if user is not None:
                auth.login(request, user)
                messages.success(request, "You are successfully logged in")
                return redirect("dashboard")
    return render(request, "accounts/user-login.html", context={"form": form})


def user_logout(request):
    # auth.logout(request)
    for key in list(request.session.keys()):
        if key == "cart_session":
            continue
        del request.session[key]
    messages.info(request, "You are successfully logged out")
    return redirect("user-login")


@login_required(login_url="user-login")
def dashboard(request):
    return render(request, "accounts/dashboard.html")


@login_required(login_url="user-login")
def profile(request):
    # image file too
    user_form = UpdateUserForm(instance=request.user)
    if request.method == "POST":
        user_form = UpdateUserForm(request.POST, request.FILES, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            messages.info(request, "Profile updated successfully")
            return redirect("dashboard")
    context = {"user_form": user_form}
    return render(request, "accounts/profile.html", context=context)


@login_required(login_url="user-login")
def delete_account(request):
    if request.method == "POST":
        user = request.user
        user.delete()
        auth.logout(request)
        messages.error(request, "Account deleted successfully")
        return redirect("user-login")
    return render(request, "accounts/delete-account.html")


@login_required(login_url="user-login")
def manage_shipping(request):
    try:
        shipping = ShippingAddress.objects.get(user=request.user)
    except ShippingAddress.DoesNotExist:
        shipping = None
    
    form = ShippingForm(instance=shipping)

    if request.method == "POST":
        form = ShippingForm(request.POST, instance=shipping)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = request.user
            
            form.save()
            messages.success(request, "Shipping address updated successfully")
            return redirect("dashboard")

    return render(request, "accounts/manage-shipping.html", {'form': form})


@login_required(login_url="user-login")
def manage_orders(request):
    user = request.user
    orders = user.order_set.all()
    return render(request, "accounts/manage-orders.html",{'orders': orders})