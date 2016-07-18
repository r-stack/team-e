# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('postermaker', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Politician',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('twitter_account', models.CharField(default='', max_length=30)),
                ('manifest', models.CharField(default='', max_length=30, null=True)),
            ],
        ),
        migrations.DeleteModel(
            name='Manifest',
        ),
        migrations.RemoveField(
            model_name='category',
            name='count',
        ),
        migrations.RemoveField(
            model_name='category',
            name='twitter_account',
        ),
        migrations.AlterField(
            model_name='category',
            name='keyword',
            field=models.CharField(default='', max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='category',
            name='politician',
            field=models.ForeignKey(default=None, to='postermaker.Politician'),
        ),
    ]
