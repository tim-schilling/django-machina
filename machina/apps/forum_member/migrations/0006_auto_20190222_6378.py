# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum_member', '0005_auto_20170628_1945'),
    ]

    operations = [
        migrations.AddField(
            model_name='forumprofile',
            name='auto_subscribe_posts',
            field=models.BooleanField(default=False, verbose_name='Automatically subscribe to topics that you post to.'),
        ),
    ]
