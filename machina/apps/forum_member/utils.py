# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from datetime import timedelta

from django.contrib.sites.models import Site
from django.utils import timezone

from machina.apps.forum_member.emails import NotificationEmail
from machina.core.db.models import get_model


Post = get_model('forum_conversation', 'Post')


def send_notifications(interval, email_class=NotificationEmail, context=None):
    """
    Send notification on email to the user that subscribe on topics.
    """

    email = email_class()

    if not context:
        context = {}

    time_ago = timezone.now() - timedelta(seconds=interval)
    for post in Post.objects.filter(created__gt=time_ago):
        users = post.topic.subscribers.filter(
            forum_profile__notify_subscribed_topics=True,
            forum_profile__user__email__isnull=False
        ).exclude(id=post.poster_id)

        for user in users:
            email_context = context.copy()
            email_context.update({
                'user': user,
                'post': post,
                'topic': post.topic,
                'current_site': Site.objects.get_current(),
            })
            email.send([user.email], email_context)
