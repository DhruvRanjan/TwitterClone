# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-27 11:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('socialnetwork', '0008_auto_20160226_1946'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='profile_picture',
            field=models.ImageField(default='pictures/defaultPicture.jpg', upload_to='pictures'),
        ),
    ]
