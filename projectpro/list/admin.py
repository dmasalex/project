from django.contrib import admin

from .models import Person, Organization, Contacts
from . import models


class OrganizationInline(admin.TabularInline):
    model = Person.organization.through
    extra = 1


class ContactsInline(admin.StackedInline):
    model = models.Contacts
    extra = 1


class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_auto', 'sender')
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ['name']
    list_filter = ['name']
    inlines = [ContactsInline]


class PersonAdmin(admin.ModelAdmin):
    list_display = ('name', 'create_date', 'phone', 'display_organization', 'funct', 'access')
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ['name']
    list_filter = ['name']
    inlines = [OrganizationInline]
    exclude = ('organization',)


class ContactsAdmin(admin.ModelAdmin):
    list_display = ('email', 'display_organization')
    prepopulated_fields = {"slug": ("email",)}


admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(Contacts, ContactsAdmin)