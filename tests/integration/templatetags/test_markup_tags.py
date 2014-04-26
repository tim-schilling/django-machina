# -*- coding: utf-8 -*-

# Standard library imports
# Third party imports
from django.template import Context
from django.template.base import Template
from django.test import TestCase
from django.test.client import RequestFactory

# Local application / specific library imports


class TestRenderedTag(TestCase):
    def setUp(self):
        self.loadstatement = '{% load url from future %}{% load markup_tags %}'
        self.request_factory = RequestFactory()

    def test_can_render_a_formatted_text_on_the_fly(self):
        # Setup
        def get_rendered(value):
            request = self.request_factory.get('/')
            t = Template(self.loadstatement + '{{ value|rendered|safe }}')
            c = Context({'value': value, 'request': request})
            rendered = t.render(c)

            return rendered

        self.assertEqual(get_rendered('[b]This is a test[/b]'), '<strong>This is a test</strong>')