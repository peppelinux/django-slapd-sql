import ldap3
import ssl

SERVER_FQDN="ldap.testunical.it"
LDAP_AUTH_URL='ldaps://{}'.format(SERVER_FQDN)

LDAP_CA_CERT='example/example/certs/testunical.slapd-cacert.pem'
LDAP_BASEDN='dc=testunical,dc=it'
LDAP_USER='cn=admin,{}'.format(LDAP_BASEDN)
LDAP_PASS='slapdsecret'

def get_supported_sasl(connection):
    s = connection.server
    print(s.info.supported_sasl_mechanisms)
    print()
    print(s.info)


# get all attributes type supported in the server
def get_server_attribute_types(connection, 
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
            # attr_repr = '{}, {}, {}, {}, {}, {}'.format(attr_obj.name, 
                                                 # attr_obj.oid, 
                                                 # attr_obj.syntax,
                                                 # attr_obj.single_value, 
                                                 # attr_obj.description,
                                                 # attr_obj.min_length)
            attr_values.append((val, getattr(attr_obj, val)))
        attrs.append(attr_values)
    return attrs


# http://ldap3.readthedocs.io/searches.html?highlight=search%20filter
def generic_search(conn, basedn='ou=people,{}'.format(LDAP_BASEDN), 
                   search_filter='(objectclass=*)'):
    conn.search(search_base=basedn, 
             search_filter=search_filter,
             search_scope = ldap3.SUBTREE, 
             attributes='*', # ['cn', 'givenName'],
             )
    return conn.entries


if __name__ == '__main__':
    server = ldap3.Server(LDAP_AUTH_URL, get_info=ldap3.ALL)
    conn = ldap3.Connection(server, user=LDAP_USER, password=LDAP_PASS, auto_bind=True)
    print(conn)
    # get_server_attribute_types(c)
    print(generic_search(conn))
