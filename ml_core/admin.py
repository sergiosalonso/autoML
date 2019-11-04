from django.contrib import admin
from .models import Process, CSVFiles, AwsInstance, MLModel, ModelMachine
# Register your models here.
admin.site.register(Process)
admin.site.register(CSVFiles)
admin.site.register(AwsInstance)
admin.site.register(MLModel)
admin.site.register(ModelMachine)
