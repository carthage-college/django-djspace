from django.core.validators import *

credit_gpa_validator = RegexValidator(
    regex='^[0-9]{1,}\.[0-9]{1,2}$',
    message='Valid inputs are: eg. 4.00 or 132.5',
    code='invalid_gpa_or_credit'
)

month_year_validator = RegexValidator(
    regex='^(0[1-9]{1}|1[0-2]{1})\/2[\d]{3}$',
    message='Valid inputs are: eg. MM/YYYY',
    code='invalid_month_year'
)

four_digit_year_validator = RegexValidator(
    regex='^2[\d]{3}$',
    message='Valid inputs are: eg. 2015',
    code='invalid_four_digit_year'
)