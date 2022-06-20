# from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from accounts.forms import UserCreationForm

# Create your views here.

class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"



# def signup(response):
#     if response.method == "POST":
#         form = RegisterForm(response.POST)
#         if form.is_valid():
#             form.save()
#
#         return redirect("")
#     else:
#         form = RegisterForm()
#
#     return render(response, "accounts/signup.html", {"form": form})
