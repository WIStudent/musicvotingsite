# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('musicvoting', '0004_directory_remove'),
    ]

    operations = [
        migrations.AddField(
            model_name='directory',
            name='imported_at',
            field=models.DateTimeField(default=None, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='directory',
            name='locked',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='directory',
            name='number_of_imported_files',
            field=models.IntegerField(default=None, null=True, blank=True),
            preserve_default=True,
        ),
    ]
