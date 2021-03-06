# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-10-01 11:22
from __future__ import unicode_literals

from django.db import migrations, models


def mark_existing_posts_as_sent(apps, schema_editor):
    Post = apps.get_model('forum_conversation', 'Post')
    for post in Post.objects.filter(approved=True):
        post.notifications_sent = True
        post.save()


class Migration(migrations.Migration):

    dependencies = [
        ('forum_conversation', '0011_remove_post_poster_ip'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='notifications_sent',
            field=models.BooleanField(default=False, verbose_name='Notifications sent'),
        ),
        migrations.RunPython(
            mark_existing_posts_as_sent,
            migrations.RunPython.noop
        ),

    ]
