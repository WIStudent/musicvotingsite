# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('musicvoting', '0005_auto_20150321_0005'),
    ]

    operations = [
        migrations.AddField(
            model_name='directory',
            name='subdirectories',
            field=models.ManyToManyField(to='musicvoting.Directory'),
            preserve_default=True,
        ),
    ]
