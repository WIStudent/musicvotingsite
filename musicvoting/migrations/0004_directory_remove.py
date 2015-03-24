# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('musicvoting', '0003_directory'),
    ]

    operations = [
        migrations.AddField(
            model_name='directory',
            name='remove',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
