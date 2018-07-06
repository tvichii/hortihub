from django.test import TestCase
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib import auth
from feed.models import UserPost

class CreatePostViewTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username='Chitra', password='password123')

    def setUp(self):
        login = self.client.login(username='Chitra', password='password123')
        user = auth.get_user(self.client)
        assert user.is_authenticated

    def test_feed_createpost_page_status_code(self):
        """
        Test that a Feed page is rendering correctly
        """
        response = self.client.get(reverse_lazy('feed:userfeed'))
        self.assertEquals(response.status_code, 200, 'Error loading feed page')
        self.assertTemplateUsed(response, 'feed/userpost_form.html')

    def test_createpost__method(self):
        """
        Test that a Userprofile is updated correctly after post
        """
        resp = self.client.post(reverse_lazy('feed:userfeed'), {'post_body':'Hello'})
        self.assertEqual(resp.status_code, 302) #redirect to same feed
        post = UserPost.objects.get(pk=1)
        self.assertEqual(post.post_body, 'Hello')

