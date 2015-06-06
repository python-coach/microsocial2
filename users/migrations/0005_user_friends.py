# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_userwallpost'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='friends',
            field=models.ManyToManyField(related_name='friends_rel_+', verbose_name='\u0434\u0440\u0443\u0437\u044c\u044f', to=settings.AUTH_USER_MODEL, blank=True),
            preserve_default=True,
        ),
    ]
