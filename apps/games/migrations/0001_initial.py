# Generated by Django 3.1.4 on 2021-04-02 20:26

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('time_started', models.DateTimeField()),
                ('time_ended', models.DateTimeField()),
                ('uuid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False)),
                ('type', models.CharField(choices=[('pu', 'Pickup Game'), ('ma', 'Marathon Game'), ('tm', 'Tournament Game')], default='pu', max_length=2)),
                ('team_one_score', models.SmallIntegerField()),
                ('team_two_score', models.SmallIntegerField()),
                ('confirmed', models.BooleanField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Point',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('uuid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False)),
                ('type', models.CharField(choices=[('sg', 'Single Point'), ('tk', 'Tink'), ('sk', 'Sink'), ('bs', 'Bounce Sink'), ('ps', 'Partner Sink'), ('ss', 'Self Sink'), ('ff', 'Fifa'), ('fg', 'Field Goal')], default='sg', max_length=2)),
                ('scored_on_position', models.SmallIntegerField(blank=True, null=True)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='game', to='games.game')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
