from django import forms
from .models import *
from django.core.exceptions import ValidationError


class OrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = ['name', 'sender', 'is_auto']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'is_auto': forms.CheckboxInput(),
            'sender': forms.TextInput(attrs={'class': 'form-control'})
        }

    def clean_slug(self):
        new_slug = self.cleaned_data['slug'].lower()

        if new_slug == 'create':
            raise ValidationError('Slug may not be "Create"')
        if Organization.objects.filter(slug__iexact=new_slug).count():
            raise ValidationError('Slug must be unique. We have "{}" slug already'.format(new_slug))
        return new_slug


class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = [
            'name',
            'position',
            'email',
            'phone',
            'document',
            'series',
            'number',
            'date_of_issue',
            'organ',
            'place_of_life',
            'date_of_birth',
            'place_of_birth',
            'funct',
            'access',
            'organization'
        ]

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'position': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.NumberInput(attrs={'class': 'form-control'}),
            'document': forms.TextInput(attrs={'class': 'form-control'}),
            'series': forms.NumberInput(attrs={'class': 'form-control'}),
            'number': forms.NumberInput(attrs={'class': 'form-control'}),
            'date_of_issue': forms.DateInput(attrs={'class': 'form-control'}),
            'organ': forms.TextInput(attrs={'class': 'form-control'}),
            'place_of_life': forms.TextInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control'}),
            'place_of_birth': forms.DateInput(attrs={'class': 'form-control'}),
            'funct': forms.TextInput(attrs={'class': 'form-control'}),
            'access': forms.TextInput(attrs={'class': 'form-control'}),
            'organization': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }

        def clean_slug(self):
            new_slug = self.cleaned_data['slug'].lower()

            if new_slug == 'create':
                raise ValidationError('Slug may not be "Create"')
            return new_slug


class LoginForm(forms.Form):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'forms-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'forms-input'}))


class ContactsForm(forms.ModelForm):
    class Meta:
        model = Contacts

        fields = ['email', 'organization']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'organization': forms.Select(attrs={'class': 'form-control'}),
        }

        def clean_slug(self):
            new_slug = self.cleaned_data['slug'].lower()

            if new_slug == 'create':
                raise ValidationError('Slug may not be "Create"')
            return new_slug
