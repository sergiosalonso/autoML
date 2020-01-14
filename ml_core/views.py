from django.shortcuts import render, reverse, get_object_or_404
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, ListView, RedirectView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Process, CSVFiles, AwsInstance
from .rpc_client import MLRpcClient
import threading
import time
import paramiko
import os
import pickle
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
import xgboost as xgb
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LinearRegression
from sklearn.metrics import auc, accuracy_score, confusion_matrix, mean_squared_error
class CreateProcess(LoginRequiredMixin, CreateView):
    model = Process
    fields = ('title', 'description', 'test', 'csv', 'model', 'machine', 'target')
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
        return super().form_valid(form)

class UpdateProcess(LoginRequiredMixin,UpdateView):
    model = Process
    fields = ('title', 'description', 'test', 'csv', 'model', 'machine', 'target')
    template_name='process/update_process.html'
    def get_success_url(self):
        return reverse('ml_core:list-process')

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

class ListProcesses(LoginRequiredMixin,ListView):
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

class ListCSV(LoginRequiredMixin,ListView):
    model=CSVFiles
    context_object_name='csv_list'
    template_name='process/list_csv.html'
    def get_queryset(self):
        '''
            Filter by user
        '''
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user.id)

class CreateCSV(LoginRequiredMixin, CreateView):
    model = CSVFiles
    fields = ('file',)
    template_name='process/create_csv.html'

    def get_success_url(self):
        return reverse('ml_core:list-csv')

    def form_valid(self, form):
        '''
            Add user who creates the
            Add validation and execute process
        '''
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()

        return super().form_valid(form)

class DeleteCSV(LoginRequiredMixin,DeleteView):
    model=CSVFiles
    success_url= reverse_lazy('ml_core:list-csv')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user.id)
'''
class CreateConfiguration(LoginRequiredMixin, CreateView):
    model = Configurations
    fields = ('process','model', 'machine')
    template_name='process/create_configuration.html'
'''
class CreateInstance(LoginRequiredMixin, CreateView):
    model = AwsInstance
    fields = ('name', 'public_ip')
    template_name='process/create_instance.html'

    def get_success_url(self):
        return reverse('ml_core:list-process')

    def form_valid(self, form):
        '''
            Add user who creates the
            Add validation and execute process
        '''
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        autostart(self.object.public_ip)
        self.object.save()
        print(self.object.public_ip)
        return super().form_valid(form)

class UpdateInstance(LoginRequiredMixin,UpdateView):
    model = AwsInstance
    fields = ('name','public_ip')
    template_name='process/update_instance.html'
    def get_success_url(self):
        return reverse('ml_core:list-instance')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user.id)

class DeleteInstance(LoginRequiredMixin,DeleteView):
    model=AwsInstance
    success_url= reverse_lazy('ml_core:list-instance')
    template_name='process/delete_instance.html'
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user.id)

class ListInstances(LoginRequiredMixin,ListView):
    model=AwsInstance
    context_object_name='instance_list'
    template_name='process/list_instances.html'
    def get_queryset(self):
        '''
            Filter by user
        '''
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user.id)

response=[]
class RPCRecieverTest(LoginRequiredMixin, TemplateView):
    template_name = "process/rpc.html"
    model=Process

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #context['model']=self.kwargs['model']
        #context['machine']=self.kwargs['machine']
        #print(type(self.kwargs['machine']))
        process= Process.objects.get(pk=self.kwargs['pk'])
        print(process.machine.public_ip)
        print(process.csv)
        pd_csv=pd.read_csv(process.csv.file)
        thread1 = threading.Thread(target = execute_server_code, args = (process.machine.public_ip,))
        thread2 = threading.Thread(target = rpc, args = (process.model.name, pd_csv, process.target, process.test,))

        thread1.start()
        thread2.start()
        thread2.join()
        thread1.join()

        task=response.pop()
        print(len(response))
        if task:
            print(type(task))
            task=pickle.loads(task)
            context['message']=task['score']
            context['machine']=process.machine.public_ip
            context['model']=process.model.name
            context['csv']=process.csv.name
            pickle.dump(task['model'], open('media/model/'+task['name']+".pkl", 'wb'))
            context['model_binary']='../../media/model/'+task['name']+".pkl"
        process.model_binary='model/'+task['name']+".pkl"
        process.save()

        return context

def execute_server_code(machine):

    print('Conectando')
    ssh = paramiko.SSHClient()
    k=paramiko.RSAKey.from_private_key_file('ml_core/cluster1.pem')
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    print('Conectando')
    #ec2-184-72-96-38.compute-1.amazonaws.com
    ssh.connect(hostname=machine, username='ubuntu', pkey=k)
    print('Lanzando comando')
    #scp_command='scp -i ml_core/cluster1.pem media/csv/'+csv+' ubuntu@'+machine+':/home/ubuntu'
    #os.system(scp_command)
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("python3 rpc_server.py", get_pty=True, timeout=10.0)
    #time.sleep(2)
    ssh_stdin.flush()

    for line in iter(ssh_stdout.readline,""):
        print(line,end="")

    ssh.close()

def rpc(model, dataset, target, test):
    #https://stackoverflow.com/questions/31834743/get-output-from-a-paramiko-ssh-exec-command-continuously/39231690#39231690
    ml_rpc = MLRpcClient()
    print(" [x] Requesting "+model)
    if model == 'svm':
        response.append(ml_rpc.call_svm(dataset, target, test))
    elif model == 'xgboost':
        response.append(ml_rpc.call_xgboost(dataset, target, test))
    elif model == 'logistic':
        response.append(ml_rpc.call_logistic(dataset, target, test))
    elif model == 'linear':
        response.append(ml_rpc.call_linear(dataset, target, test))
    print(" [.] Got %r" % response[-1])
    return 1

def autostart(machine):
    print('Conectando')
    ssh = paramiko.SSHClient()
    k=paramiko.RSAKey.from_private_key_file('ml_core/cluster1.pem')
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    print('Conectando')

    ssh.connect(hostname=machine, username='ubuntu', pkey=k)
    print('Lanzando comando')

    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('''
    sudo apt-get update \
    && sudo apt-get --assume-yes install python3-pip \
    && sudo pip3 --no-cache-dir install xgboost \
    && sudo pip3 install numpy \
    && sudo pip3 install pandas \
    && sudo pip3 install scikit-learn \
    && sudo pip3 install pika \
    && sudo apt-get --assume-yes install rabbitmq-server \
    && sudo chmod 666 /var/lib/rabbitmq/.erlang.cookie \
    && sudo echo "JXCKPIIDBMNWHSWFMPCB" > "/var/lib/rabbitmq/.erlang.cookie" \
    && sudo chmod 600 /var/lib/rabbitmq/.erlang.cookie \
    && sudo service rabbitmq-server restart \
    && sudo rabbitmqctl stop_app \
    && sudo rabbitmqctl join_cluster rabbit@ip-172-31-85-15 \
    && sudo rabbitmqctl start_app''', get_pty=True)

    scp_command='scp -i ml_core/cluster1.pem ml_core/rpc_server.py ubuntu@'+machine+':/home/ubuntu'
    os.system(scp_command)
    ssh_stdin.flush()

    for line in iter(ssh_stdout.readline,""):
        print(line,end="")

    ssh.close()
