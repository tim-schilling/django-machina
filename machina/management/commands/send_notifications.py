# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import translation

from machina.apps.forum_member.utils import send_notifications


class Command(BaseCommand):
    help = 'Send email to users that have turned on notifications for subscribed topics.'

    def handle(self, *args, **options):
        """
        Send email to users that have turned on notifications for subscribed topics.
        """

        translation.activate(settings.LANGUAGE_CODE)
        send_notifications()
        translation.deactivate()
