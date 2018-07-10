from django.test import TestCase
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib import auth
from feed.models import UserPost
from comments.models import Comment

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


class PostDetailViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='chitra', password='password123')
        cls.post = UserPost(author=user, post_body="Test post", )
        cls.post.save()


    def setUp(self):
        login = self.client.login(username='chitra', password='password123')
        user = auth.get_user(self.client)
        assert user.is_authenticated

    def test_postdetail_view_page_status_code(self):
        """
        Test that a PostDetailView page is rendering correctly
        """
        response = self.client.get(reverse_lazy('feed:post_detail', kwargs={'pk': self.post.pk}))
        self.assertEquals(response.status_code, 200, 'post doesnt exist with pk={}'.format(self.post.pk))
        self.assertTemplateUsed(response, 'feed/post_detail.html', 'Template used is wrong')

    def test_postdetail_view_post_comment(self):
        """
        Test that a comment is posted ot post correctly
        """
        user = User.objects.get(pk=1)
        resp = self.client.post(reverse_lazy('feed:post_detail', kwargs={'pk': self.post.pk}), {'content': 'just a comment'})
        self.assertEqual(resp.status_code, 302)
        # co.refresh_from_db()
        self.assertTrue(Comment.objects.filter().exists())

