# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-25 19:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Word',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.CharField(max_length=100)),
                ('part_of_speech', models.CharField(blank=True, choices=[('іменник', 'іменник'), ('займенник', 'займенник'), ('числівник', 'числівник'), ('дієслово', 'дієслово'), ('прикметник', 'прикметник'), ('прислівник', 'прислівник'), ('прийменник', 'прийменник'), ('сполучник', 'сполучник'), ('частка', 'частка'), ('вигук', 'вигук')], max_length=30)),
            ],
        ),
    ]
