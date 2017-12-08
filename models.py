from django.db import models
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _
from model_utils.fields import AutoCreatedField, AutoLastModifiedField

from . model_fields import PositiveTinyIntegerField
#from .. import settings as app_settings


class TimeStampedEditableModel(models.Model):
    """
    An abstract base class model that provides self-updating
    ``created`` and ``modified`` fields.
    """
    created = AutoCreatedField(_('created'), editable=True)
    modified = AutoLastModifiedField(_('modified'), editable=True)

    class Meta:
        abstract = True


class Org(TimeStampedEditableModel):
    o = models.CharField(verbose_name=_('Organization'),
                                max_length=254,
                                db_index=True)
    dc = models.CharField(verbose_name=_('Domain Component'), max_length=254)

    class Meta:
        db_table = 'org'
        verbose_name = _('Org')
        verbose_name_plural = _('Orgs')

    def __str__(self):
        return self.dc


class LdapOcMappings(TimeStampedEditableModel):
    """
        objectClass to table map
    """
    name = models.CharField(verbose_name=_('name'),
                                max_length=64,
                                db_index=True)
    # qui popolare keytbl e keycol con un methodo che tratta
    # le generic relations di django content types
    keytbl = models.CharField(
                            verbose_name=_('key table'),
                            max_length=255, help_text='the table where '
                            'entities for the objectClass are held. '
                            'Ex: inetOrgPerson is for identifying people, '
                            'so it uses the persons table if desidered'
                            )
    keycol = models.CharField(
                            verbose_name=_('key table'),
                            max_length=255,
                            help_text='the table\'s primary key column name'
                            )
    create_proc = models.CharField(verbose_name=_('on create'),
                          max_length=255,
                          null=True, blank=True, default=None,
                          help_text='the SQL code when an LDAP create is called')
    delete_proc = models.CharField(verbose_name=_('on delete'),
                          max_length=255,
                          null=True, blank=True, default=None,
                          help_text='the SQL code when an LDAP delete is called')
    expect_return = PositiveTinyIntegerField(verbose_name=_('expect return'),
                          help_text='what to expect when the query is '
                          'successful (ie not an error)',
                          default=0)
    class Meta:
        db_table = 'ldap_oc_mappings'
        verbose_name = _('ldap oc mapping')
        verbose_name_plural = _('ldap oc mappings')

    def __str__(self):
        return '{} - {}'.format(self.keytbl, self.keycol)

class LdapAttrMappings(TimeStampedEditableModel):
    """
        Field definitions map (table colum = ldap type)
    """
    oc_map_id = PositiveTinyIntegerField(verbose_name=_('oc map id'),
                          help_text='refers back to the id of the relevant '
                          'objectClass in the ldap_oc_mappings table')
    name = models.CharField(verbose_name=_('name'),
                            max_length=255,
                            help_text='the LDAP attribute name'
                            )
    sel_expr = models.CharField(verbose_name=_('SELECT expr'),
                                max_length=255,
                                help_text='the SELECT $arg part of the '
                                'SQL statement')
    from_tbls = models.CharField(verbose_name=_('FROM expr'),
                                max_length=255,
                                help_text='the FROM $arg part of the '
                                'SQL statement')
    join_where = models.CharField(verbose_name=_('WHERE expr'),
                                max_length=255,
                                null=True, blank=True, default=None,
                                help_text='the WHERE ... xx.xx=yy.yy ... '
                                'part of the SQL statement if applicable. '
                                'A null is allowed if you are not doing a join.')
    add_proc = models.CharField(verbose_name=_('on CREATE expr'),
                                max_length=255,
                                null=True, blank=True, default=None,
                                help_text='the SQL code when an LDAP '
                                'create is called')
    delete_proc = models.CharField(verbose_name=_('on DELETE expr'),
                                max_length=255,
                                null=True, blank=True, default=None,
                                help_text='the SQL code when an LDAP '
                                'delete is called')
    param_order = PositiveTinyIntegerField(
                                            verbose_name=_('param order'),
                                            default=3,
                                            help_text=''
                                            )
    expect_return = PositiveTinyIntegerField(
                                            verbose_name=_('expect return code'),
                                            default=0,
                                            help_text='what to expect when the query '
                                            'is successful (ie not an error)'
                                            )
    class Meta:
        db_table = 'ldap_attr_mappings'
        verbose_name = _('ldap attribute mapping')
        verbose_name_plural = _('ldap attributes mappings')

    def __str__(self):
        return '{} - {}'.format(self.name, self.sel_expr)
