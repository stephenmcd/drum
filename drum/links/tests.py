from mezzanine.utils.tests import TestCase
from drum.links.forms import LinkForm
from django.contrib.auth.models import User
from drum.links.models import Link, Profile


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


class LinkModelsTests(TestCase):

    def test_has_link_field(self):
        l = Link()
        self.assertTrue(hasattr(l, 'link'))

    def test_has_rating_field(self):
        l = Link()
        self.assertTrue(hasattr(l, 'rating'))

    def test_has_comments_field(self):
        l = Link()
        self.assertTrue(hasattr(l, 'comments'))


class ProfileModelsTests(TestCase):

    def setUp(self):
        super(ProfileModelsTests, self).setUp()
        self.user = User.objects.get(username='test')
        self.user.profile.website = "http://test.com/"
        self.user.profile.bio = "I have a dream"
        self.user.profile.karma = 777
        self.user.profile.save()
        self.profile = Profile.objects.get(user__username="test")

    def test_has_website_field(self):
        self.assertEqual("http://test.com/", self.profile.website)

    def test_has_bio_field(self):
        p = Profile.objects.get(user__username="test")
        self.assertEqual("I have a dream", self.profile.bio)

    def test_has_bio_field(self):
        p = Profile.objects.get(user__username="test")
        self.assertEqual(777, self.profile.karma)
