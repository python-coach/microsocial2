# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewsItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(max_length=50, choices=[(b'wall_post', '\u0441\u043e\u043e\u0431\u0449\u0435\u043d\u0438\u0435 \u043d\u0430 \u0441\u0442\u0435\u043d\u0435'), (b'make_friends', '\u0441\u043e\u0437\u0434\u0430\u043d\u0438\u0435 \u0434\u0440\u0443\u0436\u0435\u0441\u0442\u0432\u0435\u043d\u043d\u043e\u0439 \u0441\u0432\u044f\u0437\u0438'), (b'break_friends', '\u0440\u0430\u0437\u0440\u044b\u0432 \u0434\u0440\u0443\u0436\u0435\u0441\u0442\u0432\u0435\u043d\u043d\u043e\u0439 \u0441\u0432\u044f\u0437\u0438')])),
                ('object_id', models.PositiveIntegerField(null=True, blank=True)),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('content_type', models.ForeignKey(blank=True, to='contenttypes.ContentType', null=True)),
                ('target', models.ForeignKey(related_name='+', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-created',),
            },
            bases=(models.Model,),
        ),
    ]
