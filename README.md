Django-slapd-sql
----------------
Django-slapd-sql aim to provide a management interface to [OpenLDAP with SQL storage backend](https://www.openldap.org/faq/data/cache/978.html).
slapd-sql will present informations stored in a RDBMS as a LDAP subtree, according to the mapped attributes configured via Django Admin. 

It aim to:

- Get a working OpenLDAP server with:
    - adeguate security by default (SASL/TLS and ACL);
    - memberof and ppolicy overlays configured for identity management case of use;
    - SQL storage backend configured for MariaDB (adaptable for PostgreSQL) instead of MDB, HDB or BDB;
- Get a Django Admin backend to map LDAP and SQL schemas and attributes using also Django Generic Relations;
- Manage the same data using http://, https://, ldaps:// without any replica or scheduled syncronization;
- Permit us to query data stored in a legacy RDBMS through LDAP (slapd-sql) and viceversa (Django views);

OpenLDAP will read and NOT write on SQL (in this implementation).


Slapd-sql
---------
Slapd-sql is not a "standard" OpenLDAP backend like MDB, BDB or HDB, it can be used when you have account informations in a RDBMS, all the informations or just some of them, and you want to get these through LDAP protocol. In a OpenLDAP server many data sources can be configured to work together at the same time, SQL is one of these. SQL backend is designed to be tunable to virtually any relational schemas without having to change source (through meta-information). It also uses ODBC to connect to RDBMSes and is highly configurable for the SQL dialects that RDBMSes may use, indeed it may be used for integration and distribution of data on different RDBMSes, OSes, hosts etc., in other words, in a high heterogeneous environment.

Other tools related to OpenLDAP 
-------------------------------
OpenLDAP setup can also be provided by another ansible-application:
- https://github.com/peppelinux/ansible-slapd-eduperson2016

This is a Django Admin manager for a OpenLDAP previously configured with the previous ansible-playbook:
- https://github.com/peppelinux/django-ldap-academia-ou-manager

Django database Setup
---------------------

Install the server
````
apt install mariadb-server
````

Create the Database
````
export DJANGO_SETTINGS_MODULE='example.settings'
export USER=$(python -c "from django.conf import settings; print(settings.DATABASES['default']['USER'])")
export PASS=$(python -c "from django.conf import settings; print(settings.DATABASES['default']['PASSWORD'])")
export DB=$(python -c "from django.conf import settings; print(settings.DATABASES['default']['NAME'])")

# create your MariaDB
export HOST='%'

# tested on Debian 10
sudo mysql -u root -e "\
CREATE USER IF NOT EXISTS '${USER}'@'${HOST}' IDENTIFIED BY '${PASS}';\
CREATE DATABASE IF NOT EXISTS ${DB} CHARACTER SET = 'utf8' COLLATE = 'utf8_general_ci';\
GRANT ALL PRIVILEGES ON ${DB}.* TO '${USER}'@'${HOST}';"
````

Django stuffs
````
./manage.py migrate
./manage.py createsuperuser
./manage.py runserver

````

Configure ODBC
--------------
Thanks to [sleeplessbeastie](https://blog.sleeplessbeastie.eu/2018/01/08/how-to-install-and-configure-mariadb-unixodbc-driver/)

Install it
````
apt install unixodbc unixodbc-dev odbcinst
````

Compile MariaDB ODBC Connector
````
apt install git cmake build-essential libssl-dev
cd mariadb-connector-c

# create a makefile, compile and install
cmake -G "Unix Makefiles" -DCMAKE_INSTALL_PREFIX=/usr/local -LH
make -j 2
make install

# install ODBC
cd ..
git clone https://github.com/MariaDB/mariadb-connector-odbc.git
cd mariadb-connector-odbc
cmake -G "Unix Makefiles" -DCMAKE_BUILD_TYPE=Release -DWITH_OPENSSL=true -DCMAKE_INSTALL_PREFIX=/usr/local -LH
make -j 2
make install

cat << EOF | sudo /etc/odbcinst.ini
[MariaDB]
Driver      = libmaodbc.so
Description = MariaDB ODBC Connector
EOF

cat << EOF | tee /etc/odbc.ini
[slapd]
Description         = MariaDB slapd
Driver              = MariaDB
Database            = slapd
Server              = 127.0.0.1
Uid                 = slapd
Password            = slapdsecret
Port                = 3306
EOF
````

ODBC tests
----------

````
isql -v slapd
echo "show tables" | iusql slapd -b
````

SQL as Database backend
-----------------------
slapd-config sql attributes:
https://github.com/openldap/openldap/blob/master/servers/slapd/back-sql/config.c#L74


- enable slapd-sql module
````

````

- create an ldif to ldapadd, eg:
````
ldapadd -Y EXTERNAL -H ldapi:/// << EOF
dn: cn=module,cn=config
cn: module
objectClass: olcModuleList
olcModuleLoad: back_sql
olcModulePath: /usr/lib/ldap

EOF
````
````

ldapadd -Y EXTERNAL -H ldapi:/// << EOF
dn: olcDatabase=sql,cn=config
objectClass: olcDatabaseConfig
objectClass: olcSqlConfig
olcSuffix: dc=mariadb
olcDbName: slapd
olcDbUser: slapd
olcDbPass: slapdsecret
olcDbHost: "127.0.0.1"
olcSqlSubtreeCond: "ldap_entries.dn LIKE CONCAT('%',?)"
olcSqlInsEntryStmt: "INSERT INTO ldap_entries (dn,oc_map_id,parent,keyval) VALUES (?,?,?,?)"
EOF

olcSqlHasLDAPinfoDnRu: no
EOF
````
[TODO]
- create some conditionals in slapd role to manage this feature

Other good features, integrations and improvements
--------------------------------------------------

- syncrepl: https://github.com/akkornel/syncrepl
- MariaDB example schemas: https://www.openldap.org/devel/cvsweb.cgi/servers/slapd/back-sql/rdbms_depend/mysql/

Resources
---------
- https://linux.die.net/man/5/slapd-sql
- http://www.openldap.org/faq/data/cache/378.html
- https://tylersguides.com/guides/openldap-online-configuration-reference/
- https://www.easysoft.com/applications/openldap/back-sql-odbc.html
- https://github.com/openldap/openldap/tree/master/servers/slapd/back-sql/rdbms_depend/mysql
- https://github.com/openldap/openldap/blob/b06f5b0493937fc28f2cc86df1d7f464aa4504d8/servers/slapd/back-sql/config.c#L225
- https://www.darold.net/projects/ldap_pg/HOWTO/x178.html
- http://www.flatmtn.com/article/setting-ldap-back-sql.html
- https://www.openldap.org/lists/openldap-technical/201704/msg00016.html
- https://serverfault.com/questions/614955/openldap-with-mysql-works-but-need-schema-advice
- http://blog.mikotek.com.tw/2014/05/31/openldap-with-microsoft-sql-server-backend-database-on-centos/

- https://gist.github.com/mahirrudin/9b7754e54f1e8e532049484864beba42

Other interesting and related stuffs:
- https://github.com/openstack/ldappool (LDAP pools for foreign connections)

NBD Resources
-------------

- https://www.yumpu.com/en/document/read/35014167/openldap-and-mysql-bridging-the-data-model-divide-ukuug
- https://linux.die.net/man/5/slapd-ndb
- https://mysqlhighavailability.com/accessing-the-same-data-through-ldap-and-sql/


Others
------
- https://lsc-project.org

Status
------
Still in huge development, see you soon :)
