# Generated by Django 2.2.6 on 2019-11-10 12:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ml_core', '0010_process_models'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mlmodel',
            name='ml_models',
        ),
        migrations.RemoveField(
            model_name='process',
            name='models',
        ),
        migrations.AddField(
            model_name='process',
            name='machine',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='instance', to='ml_core.AwsInstance'),
        ),
        migrations.AddField(
            model_name='process',
            name='model',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='model', to='ml_core.MLModel'),
        ),
        migrations.DeleteModel(
            name='Configurations',
        ),
    ]