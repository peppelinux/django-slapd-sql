from django.contrib import admin
from . models import *


class TimeStampedEditableAdmin(admin.ModelAdmin):
    """
    ModelAdmin for TimeStampedEditableModel
    """

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super(TimeStampedEditableAdmin, self).get_readonly_fields(request, obj)
        return readonly_fields + ('created', 'modified')


@admin.register(LdapOcMapping)
class LdapOcMappingAdmin(TimeStampedEditableAdmin):
    pass


@admin.register(LdapAttrMapping)
class LdapAttrMappingAdmin(TimeStampedEditableAdmin):
    pass


@admin.register(LdapEntry)
class LdapEntryAdmin(TimeStampedEditableAdmin):
    pass


@admin.register(LdapEntriesObjectClasses)
class LdapEntriesObjectClassesAdmin(TimeStampedEditableAdmin):
    pass
