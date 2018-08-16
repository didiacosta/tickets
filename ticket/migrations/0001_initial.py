# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.db.models.deletion
import ticket.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Foto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('foto', models.FileField(null=True, upload_to='tickets')),
                ('fechaCreacion', models.DateTimeField(auto_now_add=True)),
                ('numeroFoto', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidadFotos', models.IntegerField(default=1)),
                ('completado', models.BooleanField(default=False)),
                ('fechaCreacion', models.DateTimeField(auto_now_add=True)),
                ('fechaActualizacion', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL, on_delete=django.db.models.deletion.PROTECT)),
            ],
        ),
        migrations.AddField(
            model_name='foto',
            name='ticket',
            field=models.ForeignKey(to='ticket.Ticket', related_name='foto_ticket', on_delete=django.db.models.deletion.PROTECT),
        ),
    ]
