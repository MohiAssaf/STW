
from django.urls import reverse
from django import test as django_test
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from ShareTheWorld.accounts.models import Profile



# ----------- profile/user tests -----------#
UserModel = get_user_model()

class ProfileRegisterViewTests(django_test.TestCase):
    VALID_DATA_FOR_REGISTER = {
        'username': 'mo',
        'password1': '12',
        'password2': '12',
        'first_name': 'mohamed',
        'last_name': 'assaf',
        'date_of_birth': '2020-09-29',
        'description': 'Bio of profile user',
        'picture': 'http://test.picture/url.png',
    }

    INVALID_USER_CREDENTIALS = {
        'username': 'mo@@',
        'password': '12SDSA',
    }



    def test_signup_page(self):
        response = self.client.get("/accounts/register/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='accounts/profile_create.html')

    def test_signup_page_view(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='accounts/profile_create.html')

    def test__when_all_valid__expect_to_create_profile(self):
        response = self.client.post(reverse('register'), data=self.VALID_DATA_FOR_REGISTER)
        self.assertEqual(response.status_code, 302)

        users = get_user_model().objects.all()
        self.assertEqual(users.count(), 1)

    def test__when_all_valid__expect_to_redirect_to_profile_details(self):
        response = self.client.post(
            reverse('register'),
            data=self.VALID_DATA_FOR_REGISTER,
        )

        expected_url = reverse('login user')
        self.assertRedirects(response, expected_url)


    def test_when_creating_profile_entering_invalid_user_credentials__expect_raise(self):
        user = UserModel.objects.create_user(**self.INVALID_USER_CREDENTIALS)

        with self.assertRaises(ValidationError) as context:
            user.full_clean()
            user.save()

        self.assertIsNotNone(context.exception)


# ----------- profile  tests -----------#
class ProfileViewTest(django_test.TestCase):
    VALID_USER_CREDENTIALS = {
        'username': 'mo',
        'password': '12',
    }

    VALID_DATA_FOR_PROFILE = {
        'first_name': 'mohamed',
        'last_name': 'assaf',
        'date_of_birth': '2003-09-26',
        'description': 'Bio of profile user',
        'picture': 'http://test.picture/url.png',
    }

    def __get_response_for_profile(self, profile):
        return self.client.get(reverse('profile details', kwargs={'pk': profile.pk}))

    def test_profile_full_name__when_valid__expect_correct_full_name(self):
        profile = Profile(**self.VALID_DATA_FOR_PROFILE)
        expected_fullname = f'{self.VALID_DATA_FOR_PROFILE["first_name"]} {self.VALID_DATA_FOR_PROFILE["last_name"]}'

        self.assertEqual(expected_fullname, profile.full_name)

    def test_expect_correct_profile_detail_view(self):
        user = UserModel.objects.create_user(**self.VALID_USER_CREDENTIALS)
        profile = Profile.objects.create(
            **self.VALID_DATA_FOR_PROFILE,
            user=user,
        )
        self.__get_response_for_profile(profile)
        self.assertTemplateUsed('accounts/profile_details.html')

    def test_when_opening_non_existing_profile__expect_error_404(self):
        response = self.client.get(reverse('profile details', kwargs={'pk': '11'}))
        self.assertEqual(404, response.status_code)



# ------- Tests for only letters validator ----#
class ProfileNameOnlyLettersValidatorTest(django_test.TestCase):
    VALID_USER_CREDENTIALS = {
        'username': 'mo',
        'password': '12',
    }

    VALID_DATA_FOR_PROFILE = {
        'first_name': 'mohamed',
        'last_name': 'assaf',
        'date_of_birth': '2003-09-26',
        'description': 'Bio of profile user',
        'picture': 'http://test.picture/url.png',
    }

    INVALID_PROFILE_NAME_CONTAINING_SPACE = {
        'first_name': 'm o',
        'last_name': 'as saf',
        'date_of_birth': '2003-09-26',
        'description': 'Bio of profile user',
        'picture': 'http://test.picture/url.png',
    }

    INVALID_PROFILE_NAME_CONTAINING_NUMBER = {
        'first_name': 'mo1',
        'last_name': 'assaf1',
        'date_of_birth': '2003-09-26',
        'description': 'Bio of profile user',
        'picture': 'http://test.picture/url.png',
    }

    INVALID_PROFILE_NAME_CONTAINING_DASH = {
        'first_name': 'mo-assaf',
        'last_name': 'as-saf',
        'date_of_birth': '2003-09-26',
        'description': 'Bio of profile user',
        'picture': 'http://test.picture/url.png',
    }

    def test_when_creating_profile_entering_only_letters__expect_success(self):
        user = UserModel.objects.create_user(**self.VALID_USER_CREDENTIALS)
        profile = Profile.objects.create(
            **self.VALID_DATA_FOR_PROFILE,
            user=user,
        )

        profile.save()
        self.assertIsNotNone(profile.pk)

    def test_when_creating_profile_entering_space_between_letters__expect_raise(self):
        user = UserModel.objects.create_user(**self.VALID_USER_CREDENTIALS)
        profile = Profile.objects.create(
            **self.INVALID_PROFILE_NAME_CONTAINING_SPACE,
            user=user,
        )
        with self.assertRaises(ValidationError) as context:
            profile.full_clean()
            profile.save()

        self.assertIsNotNone(context.exception)

    def test_when_creating_profile_entering_number_and_letters__expect_raise(self):
        user = UserModel.objects.create_user(**self.VALID_USER_CREDENTIALS)
        profile = Profile.objects.create(
            **self.INVALID_PROFILE_NAME_CONTAINING_NUMBER,
            user=user,
        )

        with self.assertRaises(ValidationError) as context:
            profile.full_clean()
            profile.save()

        self.assertIsNotNone(context.exception)

    def test_when_creating_profile_entering_dash_and_letters__expect_raise(self):
        user = UserModel.objects.create_user(**self.VALID_USER_CREDENTIALS)
        profile = Profile.objects.create(
            **self.INVALID_PROFILE_NAME_CONTAINING_DASH,
            user=user,
        )

        with self.assertRaises(ValidationError) as context:
            profile.full_clean()
            profile.save()

        self.assertIsNotNone(context.exception)




# ------- Tests for Min and Max Validators --- #

class MinDateValidatorTest(django_test.TestCase):
    VALID_USER_CREDENTIALS = {
        'username': 'mo',
        'password': '12',
    }

    VALID_DATA_FOR_PROFILE = {
        'first_name': 'mohamed',
        'last_name': 'assaf',
        'date_of_birth': '2003-01-01',
        'description': 'Bio of profile user',
        'picture': 'http://test.picture/url.png',
    }

    INVALID_DATA_FOR_PROFILE = {
        'first_name': 'mohamed',
        'last_name': 'assaf',
        'date_of_birth': '1900-01-01',
        'description': 'Bio of profile user',
        'picture': 'http://test.picture/url.png',
    }

    def test_correct_date_entered__expect_success(self):

        user = UserModel.objects.create_user(**self.VALID_USER_CREDENTIALS)
        profile = Profile.objects.create(
            **self.VALID_DATA_FOR_PROFILE,
            user=user,
        )
        profile.save()
        self.assertIsNotNone(profile.pk)

    def test_when_below_min_date_is_given__expect_to_raise(self):

        user = UserModel.objects.create_user(**self.VALID_USER_CREDENTIALS)
        profile = Profile.objects.create(
            **self.INVALID_DATA_FOR_PROFILE,
            user=user,
        )
        with self.assertRaises(ValidationError):
            profile.save()
            profile.full_clean()


class ProfileMaxDateValidatorTest(django_test.TestCase):
    VALID_USER_CREDENTIALS = {
        'username': 'mo',
        'password': '12',
    }

    VALID_DATA_FOR_PROFILE = {
        'first_name': 'mohamed',
        'last_name': 'assaf',
        'date_of_birth': '2003-01-01',
        'description': 'Bio of profile user',
        'picture': 'http://test.picture/url.png',
    }

    INVALID_DATA_FOR_PROFILE = {
        'first_name': 'mohamed',
        'last_name': 'assaf',
        'date_of_birth': '3000-01-01',
        'description': 'Bio of profile user',
        'picture': 'http://test.picture/url.png',
    }

    def test_when_correct_date__expect_success(self):
        user = UserModel.objects.create_user(**self.VALID_USER_CREDENTIALS)
        profile = Profile.objects.create(
            **self.VALID_DATA_FOR_PROFILE,
            user=user,
        )
        profile.save()
        self.assertIsNotNone(profile.pk)

    def test_when_above_max_date_is_given__expect_to_raise(self):
        user = UserModel.objects.create_user(**self.VALID_USER_CREDENTIALS)
        profile = Profile.objects.create(
            **self.INVALID_DATA_FOR_PROFILE,
            user=user,
        )
        with self.assertRaises(ValidationError):
            profile.save()
            profile.full_clean()



