from django.test import TestCase
from django.urls import reverse_lazy, reverse
from django.contrib.auth.models import User
from .forms import UserForm, ProfileForm
import datetime


class SignUpTests(TestCase):

    def test_signup_page_status_code(self):
        """
               Test that a signup page is renderign correctly
        """
        response = self.client.get('/accounts/signup/')
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/signup.html')

# class UserListViewTests(TestCase):
#
#     def test_signup_page_status_code(self):
#         """
#                Test that a signup page is renderign correctly
#         """

class UserUpdateViewTests(TestCase):

    def test_UserUpdate_page_status_code(self):
        """
        Test that a UserUpdate page is rendering correctly
        """
        user = User.objects.create_user(username='chitra',
                                        email='chitranjali@hortihub.com',
                                        password='passowrd123')
        self.assertEqual(User.objects.count(), 1)
        response = self.client.get(reverse_lazy('accounts:editprof', kwargs={'pk': user.pk}))
        self.assertEquals(response.status_code, 200,  'user doesnt exist with pk={}'.format(user.pk))
        self.assertTemplateUsed(response, 'registration/profile.html')
        login = self.client.login(username='chitra', password='passowrd123')
        valid_date_in_future = datetime.date.today() + datetime.timedelta(weeks=2)
        resp = self.client.post(reverse_lazy('accounts:editprof', kwargs={'pk': user.pk}),
                                {'date_of_birth': valid_date_in_future})
        self.assertEqual(resp.status_code, 200)
        # self.assertEqual(resp.status_code, 200)
        # self.assertRedirects(resp, reverse_lazy('home'))

