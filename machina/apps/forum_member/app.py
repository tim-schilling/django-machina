# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from machina.core.app import Application


class MemberApp(Application):
    name = 'forum_member'


application = MemberApp()
