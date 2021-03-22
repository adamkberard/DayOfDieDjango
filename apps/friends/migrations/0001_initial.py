# Generated by Django 3.1.4 on 2021-03-21 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Friend',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('PD', 'Pending'), ('DE', 'Denied'), ('AC', 'Accepted')], default='PD', max_length=2)),
                ('timeRequested', models.DateTimeField(auto_now_add=True)),
                ('timeRespondedTo', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
