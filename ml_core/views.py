from django.shortcuts import render, reverse, get_object_or_404
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, ListView, RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Process
from .rpc_client import FibonacciRpcClient
class CreateProcess(LoginRequiredMixin, CreateView):
    model = Process
    fields = ('title', 'description', 'train', 'test', 'csv', 'ml_models')
    template_name='process/create_process.html'

    def get_success_url(self):
        return reverse('ml_core:list-process')

    def form_valid(self, form):
        '''
            Add user who creates the
            Add validation and execute process
        '''
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        fibonacci_rpc = FibonacciRpcClient()
        response1 = fibonacci_rpc.call_fibo(30)
        print(" [.] Got %r" % response1)

        return super().form_valid(form)

class UpdateProcess(LoginRequiredMixin,UpdateView):
    model = Process
    fields = ('title', 'description', 'train', 'test', 'csv', 'ml_models')
    template_name='process/update_process.html'
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user.id)

class DeleteProcess(LoginRequiredMixin,DeleteView):
    model=Process
    success_url= reverse_lazy('ml_core:list-process')
    template_name='process/delete_process.html'
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user.id)

class ListProcesses(ListView):
    model=Process
    context_object_name='process_list'
    template_name='process/list_process.html'
    def get_queryset(self):
        '''
            Filter by user
        '''
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user.id)
class DetailProcess(LoginRequiredMixin,DetailView):
    model=Process
    template_name='process/detail_process.html'
