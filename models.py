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


# class Org(TimeStampedEditableModel):
    # o = models.CharField(verbose_name=_('Organization'),
                                # max_length=254,
                                # db_index=True)
    # dc = models.CharField(verbose_name=_('Domain Component'), max_length=254)
# 
    # class Meta:
        # db_table = 'org'
        # verbose_name = _('Org')
        # verbose_name_plural = _('Orgs')
# 
    # def __str__(self):
        # return self.dc


class LdapOcMapping(TimeStampedEditableModel):
    """
        objectClass to table map
        objectClass mappings: these may be viewed as structuralObjectClass, 
        the ones that are used to decide how to build an entry
    """
    name = models.CharField(verbose_name=_('name'),
                                max_length=64,
                                db_index=True,
                                help_text='the name of the objectClass; '
                                          'it MUST match the name of an '
                                          'objectClass that is loaded in '
                                          'slapd\'s schema')
    # qui popolare keytbl e keycol con un methodo che tratta
    # le generic relations di django content types
    keytbl = models.CharField(
                            verbose_name=_('key table'),
                            max_length=255, 
                            help_text='the table where '
                                      'entities for the objectClass are held. '
                                      'The name of the table that is referenced '
                                      'for the primary key of an entry')
    # the name of the column in "keytbl" that contains the primary key of an entry; 
    # the pair "keytbl.keycol" uniquely identifies an entry of objectClass "id"
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


class LdapAttrMapping(TimeStampedEditableModel):
    """
        Field definitions map (table colum = ldap type)
        attributeType mappings: describe how an attributeType for a 
        certain objectClass maps to the SQL data.
    """
    oc_map = models.ForeignKey(LdapOcMapping, 
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


class LdapEntry(TimeStampedEditableModel):
    """
      entries mapping: each entry must appear in this table, with a 
      unique DN rooted at the database naming context
    """
    dn = models.CharField(verbose_name=_('Distingieshed names'),
                          max_length=254, unique=True)
    oc_map = models.ForeignKey(LdapOcMapping, 
                               help_text='refers back to the id of the relevant '
                                         'objectClass in the ldap_oc_mappings table')
    parent = models.IntegerField(help_text='what level in the LDAP tree this is '
                                           'located at, starting with 0 (zero)')
    keyval = models.IntegerField(help_text='refers back to the id of '
                                           'the relevant row of the table the data is '
                                           'contained in. These rows are identified by '
                                           'a number that is a primary key')
    
    class Meta:
        db_table = 'ldap_entries'
        unique_together = ('oc_map', 'keyval')
        verbose_name = _('Ldap entry')
        verbose_name_plural = _('Ldap entries')

    def __str__(self):
        return self.dn


class LdapEntriesObjectClasses(TimeStampedEditableModel):
    """
      entries mapping: each entry must appear in this table, with a 
      unique DN rooted at the database naming context
    """
    
    entry = models.ForeignKey(LdapEntry, 
                               help_text='refers back to the id of the relevant '
                                         'objectClass in the ldap_oc_mappings table')
    oc_name = models.CharField(verbose_name=_('ObjectClass name'),
                          max_length=254, 
                          help_text='the name of the objectClass; it MUST match the '
                                    'name of an objectClass that is loaded in '
                                    'slapd\'s schema')
    
    class Meta:
        db_table = 'ldap_entry_objclasses'
        verbose_name = _('Ldap entry objectclass')
        verbose_name_plural = _('Ldap entry objectclasses')

    def __str__(self):
        return self.entry
