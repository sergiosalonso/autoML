from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.views.generic import ListView
from django.views.generic import DetailView
from poster.models import Post
from . import forms

class SucessForm(CreateView):
    form_class= forms.UserCreateForm
    success_url = reverse_lazy('autoML:process_list')

class ListView(ListView):
    model = Post
    paginate_by = 10

class DeatilList(DetailView):
