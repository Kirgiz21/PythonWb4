from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from PIL import Image


class ProcedureType(models.Model):

    name = models.CharField(
        max_length=100, verbose_name='Назва процедури'
    )

    price = models.IntegerField(
        verbose_name='Ціна процедури'
    )

    details = models.TextField(max_length=200, verbose_name='Деталі')

    class Meta:
        ordering = ['name']
        permissions = (
            ('can_edit_procedure_type', 'Може редагувати послуги'),
            ('can_add_procedure_type', 'Може додавати послуги'),
            ('can_delete_procedure_type', 'Може видаляти послуги')
        )

    def __str__(self):
        return self.name


class Procedure(models.Model):

    date_time = models.DateTimeField(
        verbose_name='Дата та час проведення процедури'
    )

    patient = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Пацієнт'
    )

    doctor = models.ForeignKey(
        'Doctor', on_delete=models.CASCADE, verbose_name='Лікар'
    )

    procedure_type = models.ManyToManyField(
        'ProcedureType', verbose_name='Назва процедури'
    )

    LOAN_STATUS = (
        ('p', 'Заплановано'),
        ('c', 'Підтверджено'),
        ('d', 'Виконано'),
        ('o', 'Прострочено')
    )

    status = models.CharField(
        max_length=1, choices=LOAN_STATUS, default='p', verbose_name='Статус процедури'
    )

    details = models.TextField(
        max_length=200, blank=True, null=True, verbose_name='Деталі'
    )

    class Meta:
        ordering = ['date_time']
        permissions = (
            ('can_edit_procedure', 'Може редагувати процедури'),
            ('can_add_procedure', 'Може додавати процедури'),
            ('can_delete_procedure', 'Може видаляти процедури')
        )

    def __str__(self):
        return f'Пацієнт: {self.patient}, Доктор: {self.doctor}, Дата та час: {self.date_time}'

    def get_absolute_url(self):
        return reverse('procedure-detail', args=[str(self.id)])


class Doctor(models.Model):

    first_name = models.CharField(
        max_length=50, verbose_name="Ім'я"
    )

    last_name = models.CharField(
        max_length=50, verbose_name='Прізвище'
    )

    middle_name = models.CharField(
        max_length=50, verbose_name='По-Батькові'
    )

    phone = models.CharField(
        max_length=15, verbose_name='Номер телефону'
    )

    email = models.EmailField(
        max_length=30, verbose_name='Електронна адреса'
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

    specialization = models.CharField(
        max_length=4, choices=LOAN_SPECIALIZATION, verbose_name='Спеціалізація'
    )

    photo = models.ImageField(verbose_name='Фото лікаря')

    class Meta:
        ordering = ['specialization']
        permissions = (
            ('can_edit_doctor', 'Може редагувати лікарів'),
            ('can_delete_doctor', 'Може видаляти лікарів'),
            ('can_add_doctor', 'Може додавати лікарів')
        )

    def __str__(self):
        return f'{self.last_name} {self.first_name} {self.middle_name}'

    def get_absolute_url(self):
        return reverse('doctor-detail', args=[str(self.id)])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.photo.path)
        output_size = (400, 400)
        img.thumbnail(output_size)
        img.save(self.photo.path)

