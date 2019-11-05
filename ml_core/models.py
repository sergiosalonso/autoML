from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from accounts.models import User
from django.utils import timezone

class Process(models.Model):
    title = models.CharField(max_length=250, blank=False, verbose_name='Title')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Creador', related_name='created_by')
    #slug = models.SlugField(allow_unicode=True, unique=True, blank=True)
    description = models.CharField(max_length=250, blank=True, verbose_name='Description')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    train = models.FloatField()
    test = models.FloatField()
    csv = models.ForeignKey("CSVFiles", on_delete=models.SET_NULL, blank=False, null=True, related_name='csv')
    ml_models = models.ManyToManyField("ModelMachine")

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
    file = models.FileField(upload_to="csv/")

class MLModel(models.Model):
    name = models.CharField(max_length=250, blank=False, unique=True, verbose_name='Name')
    #ml_models = models.ForeignKey("AwsInstance", on_delete=models.SET_NULL, blank=True, null=True, related_name='uploaded_by')
    def __str__(self):
        return self.name

class AwsInstance(models.Model):
    name = models.CharField(max_length=250, blank=False, unique=True, verbose_name='Name')
    public_ip = models.CharField(max_length=250, blank=False, unique=True, verbose_name='ip')

    def __str__(self):
        return self.name

class ModelMachine(models.Model):
    model = models.ForeignKey("MLModel", on_delete=models.SET_NULL, blank=True, null=True, related_name='uploaded_by')
    machine = models.ForeignKey("AwsInstance", on_delete=models.SET_NULL, blank=True, null=True, related_name='uploaded_by')

    def __str__(self):
        return (self.model.name+''+self.machine.name)
