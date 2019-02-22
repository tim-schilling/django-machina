# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import pytest
from django.core.management import call_command

from machina.core.db.models import get_model
from machina.test.factories import PostFactory
from machina.test.factories import UserFactory
from machina.test.factories import create_forum
from machina.test.factories import create_topic


ForumProfile = get_model('forum_member', 'ForumProfile')


@pytest.mark.django_db
class TestSendNotificationsCommand(object):
    def test_send_auto_subscribe_topics(self, mailoutbox):
        # Setup
        u1 = UserFactory.create()
        top_level_forum = create_forum()
        # Create a topic to auto create a forum profile
        topic = create_topic(forum=top_level_forum, poster=u1)
        PostFactory.create(topic=topic, poster=u1)
        profile = ForumProfile.objects.get(user=u1)
        profile.notify_subscribed_topics = True
        profile.auto_subscribe_topics = True
        profile.save()

        # Create the actual topic with a post
        topic = create_topic(forum=top_level_forum, poster=u1)
        PostFactory.create(topic=topic, poster=u1)

        # Create a post in a topic that u1 subscribes to
        u2 = UserFactory.create()
        PostFactory.create(topic=topic, poster=u2)

        # Run & check
        call_command('send_notifications')
        assert len(mailoutbox) == 1

    def test_send_auto_subscribe_posts(self, mailoutbox):
        # Setup
        u1 = UserFactory.create()
        u2 = UserFactory.create()

        top_level_forum = create_forum()
        # Create a topic to auto create a forum profile
        topic = create_topic(forum=top_level_forum, poster=u1)
        PostFactory.create(topic=topic, poster=u1)
        PostFactory.create(topic=topic, poster=u2)
        # Verify this doesn't trigger a notification to u2
        PostFactory.create(topic=topic, poster=u1)
        call_command('send_notifications')
        assert len(mailoutbox) == 0

        profile = ForumProfile.objects.get(user=u2)
        profile.notify_subscribed_topics = True
        profile.auto_subscribe_posts = True
        profile.save()

        # Create the topic with a post
        topic = create_topic(forum=top_level_forum, poster=u1)
        PostFactory.create(topic=topic, poster=u1, notifications_sent=True)

        # Create a post in a topic that u2 will subscribe to
        PostFactory.create(topic=topic, poster=u2)

        # Create a post to notify u2
        PostFactory.create(topic=topic, poster=u1)

        # Run & check
        call_command('send_notifications')
        assert len(mailoutbox) == 1
