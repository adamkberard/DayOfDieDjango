# Generated by Django 3.1.4 on 2021-03-21 18:21

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('league', models.CharField(choices=[('BR', 'Bronze'), ('SR', 'Silver'), ('GD', 'Gold'), ('DM', 'Diamond')], default='BR', max_length=2)),
                ('status', models.CharField(choices=[('PD', 'Pending'), ('DE', 'Denied'), ('AC', 'Accepted')], default='PD', max_length=2)),
                ('timeRequested', models.DateTimeField(auto_now_add=True)),
                ('timeRespondedTo', models.DateTimeField(auto_now=True)),
                ('teamCaptain', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='teamCaptain', to=settings.AUTH_USER_MODEL)),
                ('teammate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='teammate', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
