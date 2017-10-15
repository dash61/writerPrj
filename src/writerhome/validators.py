from django.core.exceptions import ValidationError


def validate_even(value):
    if value % 2 != 0:
        raise ValidationError(
            '%(value)s is not an even number',
            params={'value': value},
        )

# Silly example to show how we do validation.
# Similar to clean_ functions, but clean is associated with a method
# on a form, not general validation.
def validate_price(value):
    price = value
    if price < 0.50:
        raise ValidationError("Bad price, too low")