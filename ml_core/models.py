from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from accounts.models import User, Profile
from django.utils import timezone

class Process(models.Model):
    title = models.CharField(max_length=250, blank=False, verbose_name='Title')
    slug = models.SlugField(allow_unicode=True, unique=True, blank=True)
    description= models.CharField(max_length=250, blank=True, verbose_name='Description')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    train = = models.FloatField()
    test = models.FloatField()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('ml_core:process_list', kwargs={'slug':self.slug})

    class Meta:
        ordering=['created','updated']
