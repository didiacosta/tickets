# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Excepciones',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('fecha_registro', models.DateTimeField(auto_now_add=True)),
                ('error', models.TextField(blank=True)),
                ('modulo', models.CharField(blank=True, max_length=100)),
            ],
            options={
                'permissions': (('can_see_excepciones', 'can see excepciones'),),
            },
        ),
    ]
