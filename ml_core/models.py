from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from accounts.models import User
from django.utils import timezone
from django.db.models.signals import post_delete
from django.dispatch import receiver
import os
class Process(models.Model):
    title = models.CharField(max_length=250, blank=False, verbose_name='Title')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Creador', related_name='created_by')
    #slug = models.SlugField(allow_unicode=True, unique=True, blank=True)
    description = models.CharField(max_length=250, blank=True, verbose_name='Description')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    test = models.IntegerField()
    target = models.CharField(max_length=250, blank=False, verbose_name='Target')
    csv = models.ForeignKey("CSVFiles", on_delete=models.SET_NULL, blank=False, null=True, related_name='csv')
    model_binary = models.FileField(upload_to="model/")
    model= models.ForeignKey("MLModel", on_delete=models.SET_NULL, blank=True, null=True, related_name='model')
    machine= models.ForeignKey("AwsInstance", on_delete=models.SET_NULL, blank=True, null=True, related_name='instance')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('ml_core:process_list', kwargs={'slug':self.slug})

    class Meta:
        ordering=['created_at','updated_at']

class CSVFiles(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='uploaded_by')
    name = models.CharField(max_length=250, blank=False, verbose_name='name')
    file = models.FileField(upload_to="csv/")

    def save(self, *args, **kwargs):
        self.name= os.path.basename(self.file.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return os.path.basename(self.file.name)

@receiver(post_delete, sender=CSVFiles)
def submission_delete(sender, instance, **kwargs):
    '''
        Delete local file when deleting
    '''
    instance.file.delete(False)

class MLModel(models.Model):
    name = models.CharField(max_length=250, blank=False, unique=True, verbose_name='Name')
    def __str__(self):
        return self.name

class AwsInstance(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='instances_from')
    name = models.CharField(max_length=250, blank=False, unique=True, verbose_name='Name')
    public_ip = models.CharField(max_length=250, blank=False, unique=True, verbose_name='ip')

    def __str__(self):
        return self.name
'''
class Configurations(models.Model):
    process = models.ForeignKey("Process", on_delete=models.SET_NULL, blank=True, null=True, related_name='process')
    configuration =

    def __str__(self):
        return (self.process.id+' '+self.model.name+' '+self.machine.name)

class Configuration(models.Model):
    model = models.ForeignKey("MLModel", on_delete=models.SET_NULL, blank=True, null=True, related_name='model')
    machine = models.ForeignKey("AwsInstance", on_delete=models.SET_NULL, blank=True, null=True, related_name='machine')
'''
