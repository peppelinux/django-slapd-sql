import ldap3

from django.conf import settings

LDAP_Server = ldap3.Server(settings.LDAP_AUTH_URL, 
                            use_ssl=True, get_info=ldap3.ALL)
LDAP_Connection = ldap3.Connection(LDAP_Server, 
                                   user=settings.LDAP_USER, 
                                   password=settings.LDAP_PASS, 
                                   auto_bind=True)

def get_attribute_types(connection,
                        values=['name',
                                'oid',
                                'syntax',
                                'single_value',
                                'description',
                                'min_length'],
                        debug=0):
    attrs = []
    for attr in connection.server.schema.attribute_types.keys():
        attr_obj = connection.server.schema.attribute_types[attr]
        attr_values = []
        for val in values:
            if debug: print('{}'.format(getattr(attr_obj, val)), end=', ')
            attr_values.append((val, getattr(attr_obj, val)))
        attrs.append(attr_values)
    return attrs
    
