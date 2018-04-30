Django-slapd-sql
----------------
Django-slapd-sql aim to provide a management interface to OpenLDAP with SQL storage backend (slapd-sql), it present informations stored in a RDBMS as a LDAP subtree, according to the mapped attributes configured via Django Admin. With its help we can:

- Get a working OpenLDAP server through ansible role, ready to use with:
    - adeguate security by default (SASL/TLS and ACL);
    - memberof and ppolicy overlays configured for identity management case of use;
    - SQL storage backend configured for MariaDB (adaptable for PostgreSQL) instead of MDB, HDB or BDB;
    - openssl easy-rsa helpers for CA manamement;
- Get a Django Admin backend to map LDAP and SQL schemas and attributes using also Django Generic Relations;
- Manage the same data using http://, https://, ldaps:// without any replica or scheduled syncronization;
- Permit us to query data stored in a legacy RDBMS through LDAP (slapd-sql) and viceversa (Django views);

Django and OpenLDAP will read and write both on the same storage: SQL. Systems will work both on the same boat with the goal to decrease management tasks, specially for smart business solutions. This app is for who doesn't want to worry about LDAP too much but still knows that they need it.


Slapd-sql
---------
Slapd-sql is not a "standard" OpenLDAP backend like MDB, BDB or HDB, it can be used when you have account informations in a RDBMS, all the informations or just some of them, and you want to get these through LDAP protocol. In a OpenLDAP server many data sources can be configured to work together at the same time, SQL is one of these. SQL backend is designed to be tunable to virtually any relational schemas without having to change source (through meta-information). It also uses ODBC to connect to RDBMSes and is highly configurable for the SQL dialects that RDBMSes may use, indeed it may be used for integration and distribution of data on different RDBMSes, OSes, hosts etc., in other words, in a high heterogeneous environment.

OpenLDAP setup 
--------------
OpenLDAP setup can also be provided by another ansible-application:
https://github.com/peppelinux/ansible-slapd-eduperson2016

[TODO] SQL as Database backend
------------------------------
slapd-config sql attributes:
https://github.com/openldap/openldap/blob/master/servers/slapd/back-sql/config.c#L74


- create an ldif to ldapadd, eg:
````
dn: olcDatabase=sql,cn=config
objectClass: olcDatabaseConfig
objectClass: olcSqlConfig
olcSuffix: dc=test
olcDatabase: sql
olcDbName: ldap
olcDbPass: ldap
olcDbUser: ldap
olcSqlSubtreeCond: "ldap_entries.dn LIKE CONCAT('%',?)"
olcSqlInsEntryStmt: "INSERT INTO ldap_entries (dn,oc_map_id,parent,keyval) VALUES (?,?,?,?)"
olcSqlHasLDAPinfoDnRu: no
````
- create some conditionals in slapd role to manage this feature

Other good features, integrations and improvements
--------------------------------------------------
ldap models backend
- https://github.com/django-ldapdb/django-ldapdb

ldap3 auth backend
- https://github.com/etianen/django-python3-ldap, no ldap sync
- https://bitbucket.org/psagers/django-auth-ldap/ 

- backup and restore procedures working in SQL, JSON and LDIF format;
- realtime web monitor over slapd-monitor backend;
- syncrepl: https://github.com/akkornel/syncrepl;


Resources
---------
- https://linux.die.net/man/5/slapd-sql
- http://www.openldap.org/faq/data/cache/378.html
- https://github.com/openldap/openldap/tree/master/servers/slapd/back-sql/rdbms_depend/mysql
- https://www.darold.net/projects/ldap_pg/HOWTO/x178.html

Other interesting and related stuffs:
- https://github.com/futurice/futurice-ldap-user-manager (nice)
- https://github.com/django-ldapdb/django-ldapdb (alternative not usefull but interesting)
- https://www.python-ldap.org/en/latest/ (Wonderfull)
- https://github.com/openstack/ldappool (LDAP pools for foreign connections)
- https://github.com/OTA-Insight/djangosaml2idp (useful to keep in mind)

Status
------
Still in huge development, see you soon :)
