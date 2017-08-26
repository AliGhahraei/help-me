# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-26 23:05
from __future__ import unicode_literals

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(max_length=280)),
                ('date', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(blank=True, max_length=254, validators=[django.core.validators.RegexValidator(message='Not a valid email', regex='^[a-z0-9._!{}$]+@[a-z].[a-z.]')])),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(blank=True, max_length=15, validators=[django.core.validators.RegexValidator(message='El número debe tener entre 9 y quince dígitos, y puede empezar opcionalmente con un signo "+"', regex='^\\+?1?+\\d{9,15}$')])),
                ('address', models.CharField(blank=True, max_length=80)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='email',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Profile'),
        ),
        migrations.AddField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author', to='users.Profile'),
        ),
        migrations.AddField(
            model_name='comment',
            name='target',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='target', to='users.Profile'),
        ),
    ]
