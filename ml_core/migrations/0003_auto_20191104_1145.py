# Generated by Django 2.2.6 on 2019-11-04 11:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ml_core', '0002_auto_20191104_1142'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='awsinstance',
            name='ml_models',
        ),
        migrations.AddField(
            model_name='mlmodel',
            name='ml_models',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='uploaded_by', to='ml_core.AwsInstance'),
        ),
    ]
