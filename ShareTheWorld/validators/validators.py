from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible

VALIDATE_ONLY_LETTERS_ERROR = 'Value must contain only letters'

def validate_only_letters(value):
    for ch in value:
        if not ch.isalpha():
            raise ValidationError(VALIDATE_ONLY_LETTERS_ERROR)




@deconstructible
class MinDateValidator:
    def __init__(self, min_date):
        self.min_date = min_date

    def __call__(self, value):
        if value < self.min_date:
            raise ValidationError(f"Date can't be before {self.min_date}")


@deconstructible
class MaxDateValidator:
    def __init__(self, max_date):
        self.max_date = max_date

    def __call__(self, value):
        if self.max_date < value:
            raise ValidationError(f"Date can't be after {self.max_date}")