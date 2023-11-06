from django import forms

from .models import BookInstance

from django.core.exceptions import ValidationError
import datetime

class RenewBookForm(forms.Form):
    renewal_date = forms.DateTimeField(help_text="Enter a date between now and 4 weeks (default 3).")
    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']
        if data.date() < datetime.date.today():
            raise ValidationError('Invalid date - renewal in past')
        if data.date() > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError('Invalide date - renewal more then 4 weeks ahead')
        return data.date()

class RenewBookModelForm(forms.ModelForm):
    class Meta():
        model = BookInstance
        fields = ['due_back']
        labels = {'due_back': 'Renewal date'}
        help_text = {'due_back': 'Enter a date between now and 4 weeks (default 3)'}
    def clean_due_back(self):
        data = self.cleaned_data['due_back']
        if data.date() < datetime.date.today():
            raise ValidationError('Invalide date - renewal in past')
        if data.date() > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError('Invalide date - renewal more than 4 weeks ahead')
        return data.date()