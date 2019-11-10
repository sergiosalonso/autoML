# Generated by Django 2.2.6 on 2019-11-10 11:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ml_core', '0007_remove_process_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='Configurations',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('machine', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='machine', to='ml_core.AwsInstance')),
                ('model', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='model', to='ml_core.MLModel')),
            ],
        ),
        migrations.RemoveField(
            model_name='process',
            name='ml_models',
        ),
        migrations.DeleteModel(
            name='ModelMachine',
        ),
        migrations.AddField(
            model_name='configurations',
            name='process',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='process', to='ml_core.Process'),
        ),
    ]
