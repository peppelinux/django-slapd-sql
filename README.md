Django-slapd-sql
----------------
Django-slapd-sql aim to provide an usable setup and a manamgent interface for OpenLDAP with SQL as storage (slapd-sql), it present informations stored in a RDBMS as an LDAP subtree, according to the mapped attributes configured via Django Admin. Its also:

- Get a working OpenLDAP server, ready to use with:
    - adeguate security by default (SASL/TLS and ACL);
    - memberof and ppolicy overlays configured for identity management case of use;
    - SQL storage backend configured for MariaDB (adaptable for PostgreSQL) instead of MDB, HDB or BDB;
- Get a Django Admin backend to map LDAP to SQL schemas and attributes;
- Manage the same data using http://, https://, ldaps:// without any replica or scheduled syncronization;
- Permits us to use data stored in a legacy RDBMS through LDAP (slapd-sql) and viceversa (Django views);

Django and OpenLDAP will read and write both on the same storage: SQL. Systems will work together on the same storage with the goal to decrease management costs, specially for smart business solutions. This app is for who doesn't want to mind about LDAP too much but still need of it, looking for a fast and ready to use solution.


Slapd-sql
---------
Slapd-sql is not a "standard" OpenLDAP backend like MDB, BDB or HDB, it can be used when you have account informations in a RDBMS, all or just some of them, and you want to get these through LDAP. In a OpenLDAP server many data sources can be configured to work at the same time, SQL is one of these. SQL backend is designed to be tunable to virtually any relational schemas without having to change source (through meta-information). It also uses ODBC to connect to RDBMSes and is highly configurable for the SQL dialects that RDBMSes may use, indeed it may be used for integration and distribution of data on different RDBMSes, OSes, hosts etc., in other words, in a high heterogeneous environment.

OpenLDAP setup 
--------------
OpenLDAP setup can also be provided by another ansible-application, repository is:
https://github.com/peppelinux/ansible-slapd-eduperson2016


Other good features, integrations and improvements
--------------------------------------------------
- ldap3 auth backend: 
      - https://github.com/etianen/django-python3-ldap, no ldap sync;
      - https://bitbucket.org/psagers/django-auth-ldap/ 
- backup and restore procedures working in SQL, JSON and LDIF format;
- realtime web monitor over slapd-monitor backend;
- syncrepl: https://github.com/akkornel/syncrepl;


Resources
---------
- https://linux.die.net/man/5/slapd-sql
- http://www.openldap.org/faq/data/cache/378.html
- https://github.com/openldap/openldap/tree/master/servers/slapd/back-sql/rdbms_depend/mysql

Interesting/related stuffs:
- https://github.com/futurice/futurice-ldap-user-manager (nice)
- https://github.com/django-ldapdb/django-ldapdb (alternative not usefull but interesting)
- https://www.python-ldap.org/en/latest/ (Wonderfull)

Status
------
Still in huge development, see you soon :)
