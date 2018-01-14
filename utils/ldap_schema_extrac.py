#!/usr/bin/env python3

import re
DEBUG=1
BASE_DIR = '/etc/ldap/schema'
LDIF_FILE = ['core.ldif', 
             'inetorgperson.ldif',
             #'cosine.ldif',
              ]

regexp_attrtype = '[^#]olcAttributeTypes: [\(\)\{\}\.\,\'\"\:\;A-Za-z0-9\ \n]*'
regexp_uid = 'olcAttributeTypes: \( (?P<uid>[0-9\.]*)[\ \n]*'
regexp_name = 'NAME\ (?P<name>[a-zA-Z\'\(\)\ 0-9]*)[\n\ ][\n\ ]*'
regexp_desc = 'DESC\ (?P<desc>[a-zA-Z0-9\/\'\ \:\;\,\.\(\{\)\}\-]*)'



def extract_ldif_attributes(file_path):
    with open(file_path) as f:
        found = re.findall(regexp_attrtype, f.read(), re.I)
        return found

def extract_uid(attribute_str):
    res = re.findall(regexp_uid, attribute_str)
    return res

def extract_name(attribute_str):
    res = re.findall(regexp_name, attribute_str)
    return res

def extract_desc(attribute_str):
    res = re.findall(regexp_desc, attribute_str)
    return res

if __name__ == '__main__':
    for ldif in LDIF_FILE:
        print('# {}'.format(ldif))
        fpath = '{}/{}'.format(BASE_DIR, ldif)
        raw_attrs = extract_ldif_attributes(fpath)
        for ra in raw_attrs:
            raw_uid = extract_uid(ra)
            raw_name = extract_name(ra)
            raw_desc = extract_desc(ra)
            
            if not raw_uid: print('Failed uid in {}: {}\n'.format(ldif, ra))
            if not raw_name: print('Failed name in {}: {}\n'.format(ldif, ra))
            if not raw_desc: print('Failed desc in {}: {}\n'.format(ldif, ra))
            if DEBUG: print(raw_uid, raw_name, raw_desc)

            
