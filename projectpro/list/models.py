from django.db import models
from django.shortcuts import reverse
from pytils import translit

from time import time


def gen_slug(s):
    new_slug = translit.slugify(s)
    return new_slug + '-' + str(int(time()))


class Organization(models.Model):
    """Организация"""

    name = models.CharField('Название организации', max_length=200, db_index=True)
    slug = models.SlugField(max_length=150, blank=True, unique=True)
    is_auto = models.BooleanField('АВТО отправка', default=True)
    sender = models.CharField('Организация отправитель писем', null=True, max_length=200, blank=True)

    def get_absolute_url(self):
        return reverse('organization_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('organization_update_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('organization_delete_url', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = gen_slug(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return '{}'.format(self.name)

    def display_contacts(self):
        return ', '.join([contacts.email for contacts in self.organization.all()[:]])

    display_contacts.short_description = "Контакты"

    class Meta:
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'
        ordering = ['name']


class Person(models.Model):
    """Сотрудники"""

    name = models.CharField('ФИО', max_length=100, db_index=True)
    create_date = models.DateField('Дата создания', auto_now_add=True)
    position = models.CharField('Должность', max_length=200, blank=True)
    email = models.EmailField('Емейл адрес', max_length=50, blank=True)
    phone = models.CharField('Номер телефона', max_length=11, blank=True)
    document = models.CharField('Документ', max_length=200, blank=True)
    series = models.CharField('Серия документа', max_length=4, blank=True)
    number = models.CharField('Номер документ', max_length=6, blank=True)
    date_of_issue = models.DateField('Дата выдачи', blank=True, null=True)
    organ = models.CharField('Орган выдаший документ', max_length=200, blank=True)
    place_of_life = models.CharField('Место регистрации', max_length=200, blank=True)
    date_of_birth = models.DateField('Дата рождения')
    place_of_birth = models.CharField('Место рождения', max_length=100, blank=True)
    organization = models.ManyToManyField(Organization, blank=True, related_name='persons')
    slug = models.SlugField(max_length=150, blank=True, unique=True)
    funct = models.TextField('Права', blank=True)
    access = models.CharField('Группа допуска по ЭБ', max_length=100, blank=True)


    def get_absolute_url(self):
        return reverse('person_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('person_update_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('person_delete_url', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = gen_slug(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return '{}'.format(self.name)

    def display_organization(self):
        return ', '.join([organization.name for organization in self.organization.all()[:]])

    display_organization.short_description = "Организация"

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'
        ordering = ['name']


class Contacts(models.Model):
    """Контакты организации"""

    email = models.EmailField('Электронный адрес', max_length=50)
    organization = models.ForeignKey(Organization, related_name='contacts', null=True, blank=True, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=150, blank=True, unique=True)

    def get_absolute_url(self):
        return reverse('contacts_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('contacts_update_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('contacts_delete_url', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = gen_slug(self.email)
        super().save(*args, **kwargs)

    def __str__(self):
        return '{}'.format(self.email)

    def display_organization(self):
        return self.organization

    display_organization.short_description = "Организация"

    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'
