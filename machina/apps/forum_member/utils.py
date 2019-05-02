# -*- coding: utf-8 -*-

from __future__ import unicode_literals


from django.contrib.sites.models import Site
from django.db.models import Q

from machina.core.db.models import get_model
from machina.core.loading import get_class


Post = get_model('forum_conversation', 'Post')
NotificationEmail = get_class('forum_member.emails', 'NotificationEmail')


def send_notifications(email_class=None, context=None):
    """
    Send notification on email to the user that subscribe on topics.
    """
    email_class = email_class or NotificationEmail
    email = email_class()

    if not context:
        context = {}

    posts = Post.objects.filter(
        approved=True,
        notifications_sent=False,
    ).select_related('topic__forum')
    for post in posts:
        users = post.topic.subscribers.filter(
            ~Q(id=post.poster_id),
            forum_profile__notify_subscribed_topics=True,
            email__isnull=False
        )

        for user in users:
            email_context = context.copy()
            email_context.update({
                'user': user,
                'post': post,
                'topic': post.topic,
                'current_site': Site.objects.get_current(),
            })
            email.send([user.email], email_context)

        post.notifications_sent = True
        post.save()
