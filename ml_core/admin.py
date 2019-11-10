from django.contrib import admin
from .models import Process, CSVFiles, AwsInstance, MLModel
# Register your models here.
admin.site.register(Process)
admin.site.register(CSVFiles)
admin.site.register(AwsInstance)
admin.site.register(MLModel)
