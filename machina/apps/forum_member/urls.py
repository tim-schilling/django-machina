"""
    Forum member URLs
    =================

    This module defines URL patterns associated with the django-machina's ``forum_member``
    application.

"""

from django.urls import path
from django.utils.translation import ugettext_lazy as _

from machina.core.loading import get_class
from machina.core.urls import URLPatternsFactory


class ForumMemberURLPatternsFactory(URLPatternsFactory):
    """ Allows to generate the URL patterns of the ``forum_member`` application. """

    app_namespace = 'forum_member'

    user_posts_list = get_class('forum_member.views', 'UserPostsView')
    forum_profile_detail_view = get_class('forum_member.views', 'ForumProfileDetailView')
    forum_profile_update_view = get_class('forum_member.views', 'ForumProfileUpdateView')
    topic_subscribe_view = get_class('forum_member.views', 'TopicSubscribeView')
    topic_unsubscribe_view = get_class('forum_member.views', 'TopicUnsubscribeView')
    topic_subscription_list_view = get_class('forum_member.views', 'TopicSubscriptionListView')
    forum_subscription_list_view = get_class('forum_member.views', 'ForumSubscriptionListView')
    forum_subscribe_view = get_class('forum_member.views', 'ForumSubscribeView')
    forum_unsubscribe_view = get_class('forum_member.views', 'ForumUnsubscribeView')

    def get_urlpatterns(self):
        """ Returns the URL patterns managed by the considered factory / application. """
        return [
            path(
                _('profile/edit/'),
                self.forum_profile_update_view.as_view(),
                name='profile_update',
            ),
            path(
                _('profile/<str:pk>/'),
                self.forum_profile_detail_view.as_view(),
                name='profile',
            ),
            path(
                _('profile/<str:pk>/posts/'),
                self.user_posts_list.as_view(),
                name='user_posts',
            ),
            path(
                _('subscriptions/'),
                self.topic_subscription_list_view.as_view(),
                name='user_subscriptions',
            ),
            path(
                _('topic/<int:pk>/subscribe/'),
                self.topic_subscribe_view.as_view(),
                name='topic_subscribe',
            ),
            path(
                _('topic/<int:pk>/unsubscribe/'),
                self.topic_unsubscribe_view.as_view(),
                name='topic_unsubscribe',
            ),

            path(
                _('forum_subscriptions/'),
                self.forum_subscription_list_view.as_view(),
                name='user_forum_subscriptions'
            ),
            path(
                _('forum/<int:pk>/subscribe/'),
                self.forum_subscribe_view.as_view(),
                name='forum_subscribe'
            ),
            path(
                _('forum/<int:pk>/unsubscribe/'),
                self.forum_unsubscribe_view.as_view(),
                name='forum_unsubscribe'
            ),
        ]


urlpatterns_factory = ForumMemberURLPatternsFactory()
