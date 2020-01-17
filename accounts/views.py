from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth import login, authenticate
from . import forms


class SignUp(CreateView):
    form_class= forms.UserCreateForm
    success_url = reverse_lazy('process:list-process')
    template_name = 'accounts/signup.html'
    def form_valid(self, form):
        to_return =super().form_valid(form)
        user=authenticate(
            username=form.cleaned_data["username"],
            password=form.cleaned_data["password1"],
        )
        login(self.request, user)
        return to_return
