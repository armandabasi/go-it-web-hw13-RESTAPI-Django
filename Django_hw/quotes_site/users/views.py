from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from .forms import RegisterForm, MyPasswordResetForm
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy


class MyLoginView(LoginView):
    extra_context = {"title": "QuoteHive: login"}


class MyLogoutView(LogoutView):
    extra_context = {"title": "QuoteHive: logout"}


# Create your views here.
class RegisterView(View):
    form_class = RegisterForm
    template_name = "users/signup.html"

    def get(self, request):
        return render(request, self.template_name, context={"form": self.form_class, "title": "QuoteHive: sign up"})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            messages.success(request, f"Welcome {username}. Your account has been successfully created!")
            return redirect(to="users:login")
        return render(request, self.template_name, context={"form": form, "title": "QuoteHive: sign up"})


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    form_class = MyPasswordResetForm
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    html_email_template_name = 'users/password_reset_email.html'
    success_url = reverse_lazy('users:password_reset_done')
    success_message = "An email with instructions to reset your password has been sent to %(email)s."
    subject_template_name = 'users/password_reset_subject.txt'
