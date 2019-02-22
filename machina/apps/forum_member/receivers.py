"""
    Forum member signal receivers
    =============================

    This module defines signal receivers.

"""

from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import F
from django.db.models.signals import post_delete, pre_save, post_save
from django.dispatch import receiver

from machina.core.db.models import get_model


User = get_user_model()

Post = get_model('forum_conversation', 'Post')
Topic = get_model('forum_conversation', 'Topic')
ForumProfile = get_model('forum_member', 'ForumProfile')


@receiver(post_save, sender=Topic)
def auto_subscribe(sender, instance, created, **kwargs):
    """ When a new topic is posted, subscribes all the subscriber of its forum to it.

    This receiver handles automatically subscribing a user to a topic, if they are
    subscribed to the forum in which the topic was created
    """
    if not created:
        # Only new topics should be considered
        return

    for subscriber in instance.forum.subscribers.all():
        instance.subscribers.add(subscriber)


@receiver(pre_save, sender=Post)
def increase_posts_count(sender, instance, **kwargs):
    """ Increases the member's post count after a post save.

    This receiver handles the update of the profile related to the user who is the poster of the
    forum post being created or updated.
    """

    if instance.poster is None:
        # An anonymous post is considered. No profile can be updated in
        # that case.
        return

    profile, dummy = ForumProfile.objects.get_or_create(user=instance.poster)
    increase_posts_count = False

    if instance.pk:
        try:
            old_instance = instance.__class__._default_manager.get(pk=instance.pk)
        except ObjectDoesNotExist:  # pragma: no cover
            # This should never happen (except with django loaddata command)
            increase_posts_count = True
            old_instance = None
        if old_instance and old_instance.approved is False and instance.approved is True:
            increase_posts_count = True
    elif instance.approved:
        increase_posts_count = True

    if increase_posts_count:
        profile.posts_count = F('posts_count') + 1
        profile.save()


@receiver(pre_save, sender=Post)
def decrease_posts_count_after_post_unaproval(sender, instance, **kwargs):
    """ Decreases the member's post count after a post unaproval.

    This receiver handles the unaproval of a forum post: the posts count associated with the post's
    author is decreased.
    """
    if not instance.pk:
        # Do not consider posts being created.
        return

    profile, dummy = ForumProfile.objects.get_or_create(user=instance.poster)

    try:
        old_instance = instance.__class__._default_manager.get(pk=instance.pk)
    except ObjectDoesNotExist:  # pragma: no cover
        # This should never happen (except with django loaddata command)
        return

    if old_instance and old_instance.approved is True and instance.approved is False:
        profile.posts_count = F('posts_count') - 1
        profile.save()


@receiver(post_delete, sender=Post)
def decrease_posts_count_after_post_deletion(sender, instance, **kwargs):
    """ Decreases the member's post count after a post deletion.

    This receiver handles the deletion of a forum post: the posts count related to the post's
    author is decreased.
    """
    if not instance.approved:
        # If a post has not been approved, it has not been counted.
        # So do not decrement count
        return

    try:
        assert instance.poster_id is not None
        poster = User.objects.get(pk=instance.poster_id)
    except AssertionError:
        # An anonymous post is considered. No profile can be updated in
        # that case.
        return
    except ObjectDoesNotExist:  # pragma: no cover
        # This can happen if a User instance is deleted. In that case the
        # User instance is not available and the receiver should return.
        return

    profile, dummy = ForumProfile.objects.get_or_create(user=poster)
    if profile.posts_count:
        profile.posts_count = F('posts_count') - 1
        profile.save()


@receiver(post_save, sender=Post)
def auto_subscribe_to_topic(sender, instance, **kwargs):
    """
    Receiver to handle automatic subscription of created topics.
    """

    try:
        assert instance.poster_id is not None
        poster = User.objects.get(pk=instance.poster_id)
    except AssertionError:
        # An anonymous post is considered. No auto susbcription is possible.
        return
    except ObjectDoesNotExist:  # pragma: no cover
        # This can happen if a User instance is deleted. In that case the
        # User instance is not available and the receiver should return.
        return

    if (instance.topic.poster == poster and hasattr(poster, 'forum_profile') and
            poster.forum_profile.auto_subscribe_topics):
        poster.topic_subscriptions.add(instance.topic)
