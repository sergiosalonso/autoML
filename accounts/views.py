from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from . import forms


class SignUp(CreateView):
    form_class= forms.UserCreateForm
    success_url = reverse_lazy('accounts:login')
    template_name = 'accounts/signup.html'
