# Django-slapd-sql

Django-slapd-sql aims to provide a setup and a smart approach in the usage of OpenLDAP with SQL storage, to present informations stored in a RDBMS as an LDAP subtree. The benefits of this approach could be summarized as follow:

- Get a working OpenLDAP server, ready to use with:
    - adeguate security by default;
    - memberof and ppolicy overlays configured for identity management case of use;
    - SQL storage backend on MariaDB (adaptable for PostgreSQL) instead of MDB, HDB or BDB;
- Get a Django Admin backend to map LDAP and SQL schemas and attributes;
- Manage the same data using http://, https://, ldaps:// without any replica or scheduled syncronization;

Django e OpenLDAP will read and write, both, on the same SQL storage, the system will work together on the same storage.

slapd-sql
---------
Slapd-sql is not a "standard" OpenLDAP backend like DMB, BDB or HDB, but it can be used when you have account informations in a RDBMS and you want to get these through LDAP. In a OpenLDAP server many data sources can be configured to work at the same time, SQL is one of these. SQL backend is designed to be tunable to virtually any relational schema without having to change source (through that meta-information mentioned). Also, it uses ODBC to connect to RDBMSes, and is highly configurable for SQL dialects RDBMSes may use, so it may be used for integration and distribution of data on different RDBMSes, OSes, hosts etc., in other words, in highly heterogeneous environment.

Resources
---------
https://linux.die.net/man/5/slapd-sql
http://www.openldap.org/faq/data/cache/378.html
https://github.com/openldap/openldap/tree/master/servers/slapd/back-sql/rdbms_depend/mysql



OpenLDAP setup can also be provided by another ansible-application, repository is:
https://github.com/peppelinux/ansible-slapd-eduperson2016

Status
------
Still in huge development, see you soon :)
