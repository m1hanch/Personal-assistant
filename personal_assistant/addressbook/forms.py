from django.core.exceptions import ValidationError
from django.forms import ModelForm, TextInput, DateField
from django.utils import timezone

from .models import Contact
from django.forms import CharField

def validate_past_date(value):
    if value > timezone.now().date():
        raise ValidationError('Only past dates are allowed.')
def validate_phone(value):
    if not value.isdigit() or (value[0] == '+' and not value[1:].isdigit()):
        raise ValidationError('Only digits are allowed.')

class ContactForm(ModelForm):
    first_name = CharField(max_length=50, required=True, widget=TextInput())
    last_name = CharField(max_length=50, widget=TextInput())
    phone = CharField(max_length=50, widget=TextInput(), validators=[validate_phone])
    email = CharField(max_length=50, widget=TextInput())
    address = CharField(max_length=150, widget=TextInput())
    birthday = DateField(widget=TextInput(), validators=[validate_past_date])
    class Meta:
        model = Contact
        fields = ['first_name', 'last_name', 'phone', 'email', 'address', 'birthday']
        exclude = ['user']
