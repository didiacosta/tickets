# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import cloudinary.models


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0004_auto_20180815_1732'),
    ]

    operations = [
        migrations.AlterField(
            model_name='foto',
            name='foto',
            field=cloudinary.models.CloudinaryField(verbose_name='image', max_length=255, null=True),
        ),
    ]
