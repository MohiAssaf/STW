from django.contrib.auth import get_user_model
from django.urls import reverse
from django import test as django_test

from ShareTheWorld.MAIN.models import Post, Plan
from ShareTheWorld.accounts.models import Profile

UserModel = get_user_model()

class PostPlansViewTests(django_test.TestCase):
    VALID_POST_DATA = {
        'owner': 'mo',
        'photo': 'http://test.picture/url.png',
        'place_visited': 'Bulgaria',
        'date_visited': '2022-09-29',
        'description': 'The best place !!',
    }

    VALID_PLAN_DATA = {
        'flag_of_place': 'http://test.picture/url.png',
        'name_of_place': 'Bulgaria',
        'budget': '555',
        'note': 'woow',
        'date_going': '2022-09-29',

    }
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


    def __get_response_for_profile(self, profile):
        return self.client.get(reverse('profile details', kwargs={'pk': profile.pk}))

    def __get_response_for_post(self, post):
        return self.client.get(reverse('post details', kwargs={'pk': post.pk}))

    def __get_response_for_plan(self, plan):
        return self.client.get(reverse('plan details', kwargs={'pk': plan.pk}))

    def __create_post_and_plan_for_user(self, user):
        post = Post.objects.create(
            **self.VALID_POST_DATA,
            user=user,
        )
        plan = Plan.objects.create(
            **self.VALID_PLAN_DATA,
            user=user,
        )
        post.save()
        plan.save()

        return (post, plan)

    def test_when_post_is_added_expect_post_count_to_be_1(self):
        user = UserModel.objects.create_user(**self.VALID_USER_CREDENTIALS)
        profile = Profile.objects.create(
            **self.VALID_DATA_FOR_PROFILE,
            user=user,
        )
        self.__create_post_and_plan_for_user(user)
        response = self.__get_response_for_profile(profile)

        self.assertEqual(1, response.context['post_count'])

    def test_when_no_posts__expect_post_count_to_be_0(self):
        user = UserModel.objects.create_user(**self.VALID_USER_CREDENTIALS)
        profile = Profile.objects.create(
            **self.VALID_DATA_FOR_PROFILE,
            user=user,
        )
        response = self.__get_response_for_profile(profile)

        self.assertEqual(0, response.context['post_count'])


    def test_when_user_is_not_owner_of_the_post__expect_is_owner_to_be_false(self):
        user = UserModel.objects.create_user(**self.VALID_USER_CREDENTIALS)
        post = Post.objects.create(
            **self.VALID_POST_DATA,
            user=user,
        )

        credentials = {
            'username': 'momom',
            'password': 'momomo11',
        }


        self.client.login(**credentials)

        response = self.__get_response_for_post(post)

        self.assertFalse(response.context['is_owner'])


    def test_when_user_is_not_owner_of_the_plan__expect_is_owner_to_be_false(self):
        user = UserModel.objects.create_user(**self.VALID_USER_CREDENTIALS)
        plan = Plan.objects.create(
            **self.VALID_PLAN_DATA,
            user=user,
        )

        credentials = {
            'username': 'momom',
            'password': 'momomo11',
        }


        self.client.login(**credentials)

        response = self.__get_response_for_plan(plan)

        self.assertFalse(response.context['is_owner'])


    def test_when_user_is__owner_of_the_post__expect_is_owner_to_be_true(self):
        user = UserModel.objects.create_user(**self.VALID_USER_CREDENTIALS)
        post = Post.objects.create(
            **self.VALID_POST_DATA,
            user=user,
        )


        self.client.login(**self.VALID_USER_CREDENTIALS)
        response = self.__get_response_for_post(post)

        self.assertTrue(response.context['is_owner'])


    def test_when_user_is_owner_of_the_plan__expect_is_owner_to_be_true(self):
        user = UserModel.objects.create_user(**self.VALID_USER_CREDENTIALS)
        plan = Plan.objects.create(
            **self.VALID_PLAN_DATA,
            user=user,
        )


        self.client.login(**self.VALID_USER_CREDENTIALS)
        response = self.__get_response_for_plan(plan)

        self.assertTrue(response.context['is_owner'])





        
