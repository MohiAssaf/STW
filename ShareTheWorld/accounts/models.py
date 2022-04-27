import datetime

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import MinLengthValidator, RegexValidator
from django.db import models

from ShareTheWorld.accounts.managers import STWUserManager
from ShareTheWorld.validators.validators import validate_only_letters, MinDateValidator, MaxDateValidator

USERNAME_ERROR_MESSAGE = "Ensure this value contains only letters, numbers, and underscore."

class STWUser(AbstractBaseUser, PermissionsMixin):
    USERNAME_MAX_LENGTH = 15
    USERNAME_MIN_LEN = 2

    username = models.CharField(
        max_length=USERNAME_MAX_LENGTH,
        unique=True,
        validators=(
            MinLengthValidator(USERNAME_MIN_LEN),
            RegexValidator('^[A-Za-z0-9_]*$', message=USERNAME_ERROR_MESSAGE),
        ),
    )

    date_joined = models.DateTimeField(
        auto_now_add=True,
    )

    is_staff = models.BooleanField(
        default=False,
    )

    USERNAME_FIELD = 'username'

    objects = STWUserManager()


class Profile(models.Model):
    FIRST_NAME_MIN_LENGTH = 3
    FIRST_NAME_MAX_LENGTH = 20

    LAST_NAME_MIN_LENGTH = 3
    LAST_NAME_MAX_LENGTH = 25

    MIN_DATE_OF_BIRTH = datetime.date(1950, 1, 1)

    MAX_DATE_OF_BIRTH = datetime.date(datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now().day)



    first_name = models.CharField(
        max_length=FIRST_NAME_MAX_LENGTH,
        validators=(
            MinLengthValidator(FIRST_NAME_MIN_LENGTH),
            validate_only_letters,
        )
    )

    last_name = models.CharField(
        max_length=LAST_NAME_MAX_LENGTH,
        validators=(
            MinLengthValidator(LAST_NAME_MIN_LENGTH),
            validate_only_letters,
        )
    )


    date_of_birth = models.DateField(
        validators=(
            MinDateValidator(MIN_DATE_OF_BIRTH),
            MaxDateValidator(MAX_DATE_OF_BIRTH),
        ),
    )

    description = models.TextField()

    picture = models.URLField()

    user = models.OneToOneField(
        STWUser,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    @property
    def age(self):
        return datetime.datetime.now().year - self.date_of_birth.year

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"



