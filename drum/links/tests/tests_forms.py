from unittest import TestCase

from drum.links.forms import LinkForm


class LinkFormsTests(TestCase):

    def test_valid_data(self):
        form = LinkForm({
            "title": "Test title",
            "link": "http://test.com/",
            "description": "Test Desc",
        })
        self.assertTrue(form.is_valid())

    def test_title_may_not_be_empty(self):
        form = LinkForm({
            "title": "",
            "link": "http://test.com/",
            "description": "Test Desc",
        })
        self.assertFalse(form.is_valid())

    def test_link_may_be_empty(self):
        form = LinkForm({
            "title": "Test title",
            "link": "",
            "description": "Test Desc",
        })
        self.assertTrue(form.is_valid())

    def test_description_may_be_empty(self):
        form = LinkForm({
            "title": "Test title",
            "link": "http://test.com/",
            "description": "",
        })
        self.assertTrue(form.is_valid())
