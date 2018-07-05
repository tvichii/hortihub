from django.test import TestCase
from django.contrib.auth.models import User
from accounts.models import Profile
import datetime

class ProfileModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        #Set up non-modified objects used by all test methods
        User.objects.create_user(username='chitra',)
        # self.profile = Profile(user=user)
        # self.profile.save()

    def test_date_of_birth_userprofile(self):
        user = User.objects.get(pk=1)
        date_of_birth = datetime.date.today()
        # profile = user.profile
        # profile.date_of_birth = date_of_birth

        profile = Profile(user=user, date_of_birth=date_of_birth)
        profile.save()
        self.assertEquals(profile.date_of_birth, datetime.date.today())

    def test_object_represent_string(self):
        user = User.objects.get(pk=1)
        profile = Profile(user=user)
        self.assertEqual(str(profile), 'Profile for user {}'.format(profile.user.username))

