from django.test import TestCase
from django.urls import reverse_lazy
from django.contrib.auth.models import User
import datetime
from django.contrib import auth

class SignUpTests(TestCase):

    def test_signup_page_status_code(self):
        """
               Test that a signup page is renderign correctly
        """
        response = self.client.get('/accounts/signup/')
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/signup.html')

class UserListViewTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Create 4 users for listview tests
        number_of_users = 4
        for user_num in range(number_of_users):
            User.objects.create_user(username='Chitra{}'.format(user_num),first_name='Chitra{}'.format(user_num), last_name='Surname{}'.format(user_num),password='passowrd{}'.format(user_num), )

    def setUp(self):
        login = self.client.login(username='Chitra1', password='passowrd1')
        user = auth.get_user(self.client)
        assert user.is_authenticated

    def test_UserListView_page_status_code(self):
        """
               Test that a UserListView page is renderign correctly
        """
        response = self.client.get(reverse_lazy('accounts:users_list'))
        self.assertEquals(response.status_code, 200, 'Error loading page')
        self.assertTemplateUsed(response, 'user/user_list.html', 'Template used is different')

class UserUpdateViewTests(TestCase):

    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(username='chitra',
                                        email='chitranjali@hortihub.com',
                                        password='passowrd123')
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(self.user.pk, 1)
        login = self.client.login(username='chitra', password='passowrd123')
        user = auth.get_user(self.client)
        assert user.is_authenticated

    def test_UserUpdate_page_status_code(self):
        """
        Test that a UserUpdate page is rendering correctly
        """
        response = self.client.get(reverse_lazy('accounts:editprof', kwargs={'pk': self.user.pk}))
        self.assertEquals(response.status_code, 200, 'user doesnt exist with pk={}'.format(self.user.pk))
        self.assertTemplateUsed(response, 'registration/profile.html')

    def test_UserUpdate_page_post_method(self):
        """
        Test that a Userprofile is updated correctly after post
        """
        date_of_birth = datetime.date.today() - datetime.timedelta(weeks=68)
        resp = self.client.post(reverse_lazy('accounts:editprof', kwargs={'pk': self.user.pk}),
                                {'date_of_birth':date_of_birth, 'last_name': 'edpuganti'})
        self.assertEqual(resp.status_code, 302)
        self.user.refresh_from_db()
        self.assertEqual(self.user.last_name, 'edpuganti')


    def test_UserUpdate_page_redirect(self):
        """
        Test to check if userprofile edit page is redirecting after post method
        """
        resp = self.client.post(reverse_lazy('accounts:editprof', kwargs={'pk': self.user.pk}),
                                {'last_name': 'edpuganti'})
        self.assertRedirects(resp, reverse_lazy('accounts:userdetail', kwargs={'pk': self.user.pk}),status_code=302, target_status_code=200)

    def tearDown(self):
        self.user.delete()
