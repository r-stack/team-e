# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('twitter_account', models.CharField(max_length=30)),
                ('keyword', models.CharField(max_length=30)),
                ('count', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Manifest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('twitter_account', models.CharField(max_length=30)),
                ('manifest_wording', models.CharField(max_length=30)),
            ],
        ),
    ]
