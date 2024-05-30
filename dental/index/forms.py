from datetime import datetime

from django import forms
from django.contrib.auth.models import User, Group
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .models import Doctor, ProcedureType


class CreateUpdateDoctorForm(forms.Form):
    first_name = forms.CharField(
        max_length=50, label="Ім'я"
    )

    last_name = forms.CharField(
        max_length=50, label='Прізвище'
    )

    middle_name = forms.CharField(
        max_length=50, label='По-Батькові'
    )

    phone = forms.CharField(
        max_length=15, label='Номер телефону'
    )

    email = forms.EmailField(
        max_length=30, label='Електронна адреса'
    )

    LOAN_SPECIALIZATION = (
        ('ther', 'Терапевтична стоматологія'),
        ('orth', 'Ортодонтія'),
        ('oral', 'Хірургічна стоматологія'),
        ('endo', 'Ендодонтія'),
        ('peri', 'Періодонтологія'),
        ('pedi', 'Педіатрична стоматологія'),
        ('pros', 'Протезування')
    )

    specialization = forms.ChoiceField(choices=LOAN_SPECIALIZATION, label='Спеціалізація')

    photo = forms.ImageField(label='Фото лікаря', required=False)


class ConfirmDeleteForm(forms.Form):
    confirm = forms.BooleanField(label="Підтвердіть видалення ")


class CreateProcedureFormForUsers(forms.Form):
    date_time = forms.DateTimeField(label='Дата та час проведення процедури (наприклад 2022-03-31 19:30:00)',
                                    input_formats=['%Y-%m-%d %H:%M:%S'])

    doctor = forms.ModelChoiceField(queryset=Doctor.objects.all(), label='Лікар')

    procedure_type = forms.ModelMultipleChoiceField(queryset=ProcedureType.objects.all(), label='Назва процедури')

    details = forms.CharField(max_length=200, label='Деталі', required=False)

    def clean_date_time(self):
        date_time = self.cleaned_data.get('date_time')
        if date_time:
            if timezone.now() > date_time:
                raise ValidationError(_('Невірна дата - дата в минулому'))
        return date_time


class CreateUpdateProcedureFormForAdmins(forms.Form):
    date_time = forms.DateTimeField(label='Дата та час проведення процедури (наприклад 2022-03-31 19:30:00)',
                                    input_formats=['%Y-%m-%d %H:%M:%S'])

    doctor = forms.ModelChoiceField(queryset=Doctor.objects.all(), label='Лікар')

    group = Group.objects.get(name='patients')
    users_in_group = group.user_set.all()

    patient = forms.ModelChoiceField(queryset=users_in_group, label='Пацієнт')

    procedure_type = forms.ModelMultipleChoiceField(queryset=ProcedureType.objects.all(), label='Назва процедури')

    LOAN_STATUS = (
        ('p', 'Заплановано'),
        ('c', 'Підтверджено'),
        ('d', 'Виконано'),
        ('o', 'Прострочено')
    )

    status = forms.ChoiceField(choices=LOAN_STATUS, label='Статус')

    details = forms.CharField(max_length=200, label='Деталі', required=False)

    def clean_date_time(self):
        date_time = self.cleaned_data.get('date_time')
        if date_time:
            if timezone.now() > date_time:
                raise ValidationError(_('Невірна дата - дата в минулому'))
        return date_time

    def __init__(self, *args, **kwargs):
        disabled_fields = kwargs.pop('disabled_fields', [])
        super().__init__(*args, **kwargs)
        for field_name in disabled_fields:
            self.fields[field_name].disabled = True
            self.fields[field_name].required = False


class CreateUpdateProcedureTypeForm(forms.Form):
    name = forms.CharField(max_length=100, label='Назва процедури')

    price = forms.IntegerField(label='Ціна процедури', min_value=0)

    details = forms.CharField(label='Деталі')

