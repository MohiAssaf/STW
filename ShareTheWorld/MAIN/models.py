from django.core.validators import MinValueValidator, MinLengthValidator
from django.db import models
from django.contrib.auth import get_user_model

from ShareTheWorld.accounts.models import STWUser
from ShareTheWorld.validators.validators import validate_only_letters

UserModel = get_user_model()

class Post(models.Model):
    OWNER_MIN_LEN = 2
    OWNER_MAX_LEN = 15

    PLACE_MAX_LEN = 20

    owner = models.CharField(
        max_length=OWNER_MAX_LEN,
        validators=(
            MinLengthValidator(OWNER_MIN_LEN),
            validate_only_letters,
        )
    )

    photo = models.URLField()


    place_visited = models.CharField(
        max_length=PLACE_MAX_LEN,
    )

    date_visited = models.DateField(
        null=True,
        blank=True,
    )


    description = models.TextField()

    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )

class Plan(models.Model):
    MAX_LENGTH_PLACE_TO_VISIT = 20
    BUDGET_MIN_VALUE = 0

    flag_of_place = models.URLField(
        verbose_name='Flag URL'
    )

    name_of_place = models.CharField(
        max_length=MAX_LENGTH_PLACE_TO_VISIT,
        verbose_name='Place visiting',
    )

    budget = models.FloatField(
        validators=(
            MinValueValidator(BUDGET_MIN_VALUE),

        ))

    note = models.TextField(
        verbose_name='Notes'
    )

    date_going = models.DateField(
        verbose_name='Date visiting',
    )

    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )


class Comment(models.Model):
    MAX_OWNER_LENGTH = 15

    MAX_LENGTH_COMMENT = 35


    post = models.ForeignKey(
        'Post',
        on_delete=models.CASCADE,
        related_name='comments',
    )

    comment_owner = models.CharField(
        max_length=MAX_OWNER_LENGTH,
        verbose_name='Your Name',
        validators=(
            validate_only_letters,
        )
    )

    comment_body = models.TextField(
        max_length=MAX_LENGTH_COMMENT,
        verbose_name='Comment'
    )

    date_posted = models.DateTimeField(
        auto_now_add=True
    )













