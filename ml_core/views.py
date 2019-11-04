from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.views.generic import ListView, DetailView
from . import forms
'''
class CreateProcess(CreateView):
    form_class= forms.UserCreateForm
    success_url = reverse_lazy('')

class ListView(ListView):
    model = Post
    paginate_by = 10
'''
