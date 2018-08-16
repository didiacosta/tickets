# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0002_auto_20180815_1241'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='foto',
            name='numeroFoto',
        ),
    ]
