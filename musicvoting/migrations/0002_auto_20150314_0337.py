# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('musicvoting', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('playing', models.BooleanField(default=False)),
                ('number_of_votes', models.IntegerField(default=0)),
                ('track', models.ForeignKey(default=None, blank=True, to='musicvoting.Track', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='user',
            name='voted_next_track',
            field=models.ForeignKey(default=None, blank=True, to='musicvoting.Player', null=True),
            preserve_default=True,
        ),
    ]
