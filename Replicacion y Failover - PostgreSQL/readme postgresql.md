# Explicación de archivos
## Bots
Estos archivos son los bots hechos en python para probar a funcinalidad de la
replicación hecha en postgresql
- leer.py
- insertar.py
- modificar.py
- eliminar.py
## Configuracion postgresql
archivos de configuracion del postgresql para permitir la replica
- pg_hba.txt
- postgresql.conf
## INSTALACIÓN DE LA ULTIMA VERSION DE POSTGRESQL EN UBUNTU SERVER 22
sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'

wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -

sudo apt-get update

sudo apt-get install -y postgresql-16 postgresql-contrib-16 postgresql-16-repmgr

sudo systemctl status postgresql

echo 'export PATH=$PATH:/usr/lib/postgresql/16/bin' >> ~/.bashrc
source ~/.bashrc

sudo su - postgres
psql -c "ALTER USER postgres WITH PASSWORD 'EXAMPLE_PASSWORD'"
```
## SSH configuración
```bash
su - postgres
ssh-keygen -t rsa -b 4096
ssh-copy-id postgres@STANDBY_IP
ssh STANDBY_IP
```
## 1 Configuración de replicación en el nodo Master
```bash
# Crea el usuario repmgr en el usuario postgres y la base repmgr
createuser -s repmgr
createdb repmgr -O repmgr

# Editar archivo dehost configuración de postgresql
nano /etc/postgresql/16/main/postgresql.conf

# Descomentar y cambiar a los siguientes valores
shared_preload_libraries = 'repmgr'
wal_level = replica
archive_mode = on
archive_command = '/bin/true'
max_wal_senders = 10
max_replication_slots = 10
hot_standby = on
listen_addresses = '*'
```
## 2 Configuración de la autentificación de clientes en el nodo Master
```bash
# Editar archivo de configuración de autentificacion de clientes
nano /etc/postgresql/16/main/pg_hba.conf

# Agregar las siguientes lineas al final del archivo, Por cada nodo esclavo se tiene que agregar la linea que tiene el STANDBY_IP/32 con su respectiva direccion IP, tanto en el primero como en el segundo
local   replication   repmgr                                    trust
host    replication   repmgr            127.0.0.1/32            trust
host    replication   repmgr            PRIMARY_IP/32           trust
host    replication   repmgr            STANDBY_IP/32           trust

local   repmgr        repmgr                                    trust
host    repmgr        repmgr            127.0.0.1/32            trust
host    repmgr        repmgr            PRIMARY_IP/32           trust
host    repmgr        repmgr            STANDBY_IP/32           trust

# Reiniciamos el servicio postgresql para que haga efecto los cambios
sudo systemctl restart postgresql

# Revisa que el servicio este funcionando correctamente con el siguiente comando
systemctl status postgresql


```
## 3 Pruebas de conexión en los nodos Slaves
```bash
# En cada nodo esclavo prueba acceder al usuario posgresql creado llamado repmgr, esto para ver que el nodo Master esta aceptando las conexiones correctamente

psql 'host=PRIMARY_IP user=repmgr dbname=repmgr connect_timeout=2'

# Tiene que salirte lo siguiente por pantalla

repmgr=#
```
## 4 Crea el archivo de configuracion de repmgr en el Nodo Master
```bash
# En el nodo master
sudo nano /etc/repmgr.conf

# Escribe lo siguiente en el archivo creado, recuerda cambiar el PRIMARY_IP por la ip del nodo master
node_id=1
node_name=pg1
conninfo='host=PRIMARY_IP user=repmgr dbname=repmgr connect_timeout=2'
data_directory='/var/lib/postgresql/16/data'
failover=automatic
promote_command='repmgr -f /etc/repmgr.conf standby promote --log-to-file'
follow_command='repmgr -f /etc/repmgr.conf standby follow --log-to-file'
log_file='/var/log/postgresql/repmgr.log'
```
## 5 Crea el archivo de configuracion de repmgr en los nodos Esclavos
```bash
# En el nodo esclavo
sudo nano /etc/repmgr.conf

# Escribe lo siguiente en el archivo creado, recuerda cambiar el STANDBY_IP por la ip del nodo esclavo en el que estas. Tambien cambia el nombre del nodename correspondiente y el id.
node_id=2
node_name=pg2
conninfo='host=STANDBY_IP user=repmgr dbname=repmgr connect_timeout=2'
data_directory='/var/lib/postgresql/16/data'
failover=automatic
promote_command='repmgr -f /etc/repmgr.conf standby promote --log-to-file'
follow_command='repmgr -f /etc/repmgr.conf standby follow --log-to-file'
log_file='/var/log/postgresql/repmgr.log'
```
## 6 Registra Nodo Master con repmgr
```bash
# En la consola del nodo Master
repmgr -f /etc/repmgr.conf primary register

# Revisa que se haya registrado correctamente en el repmgr
repmgr -f /etc/repmgr.conf cluster show

```
## 7 Registra los Nodos Esclavos en el repmgr
```bash
# Repetir este proceso en cada nodo esclavo

# Comando para ver si el nodo Esclavo esta listo para replicar al maestro, recuerda cambiar el PRIMARY_IP por la direccion del master
repmgr -h PRIMARY_IP -U repmgr -d repmgr -f /etc/repmgr.conf standby clone --copy-external-config-files --dry-run

# Debe salir el siguiente mensaje
# NOTICE: standby will attach to upstream node 1 
# ... 
# INFO: all prerequisites for "standby clone" are met

# Ahora corre el siguiente comando para registrar al nodo maestro en el nodo esclavo actual, cambia la  PRIMARY_IP por la direccion de nodo master
repmgr -h PRIMARY_IP -U repmgr -d repmgr -f /etc/repmgr.conf standby clone --copy-external-config-files

# Debe salir el siguiente mensaje
# NOTICE: standby clone (using pg_basebackup) complete
# ... 
# NOTICE: you can now start your PostgreSQL server

# Realiza uno cambios en el archivo configuración del postgresql en los nodos esclavos
nano /etc/postgresql/16/main/postgresql.conf

# Cambia lo siguiente en el nodo esclavo
data_directory = '/var/lib/postgresql/16/data'

# Reinicia el servicio postgresql del nodo esclavo actual y luego verifica el status

sudo systemctl restart postgresql

sudo systemctl status postgresql
```
## 8 Revisa en el nodo Master que las conexiones estén realizada
```bash
# Corran los siguientes comandos en el nodo master para revisar que os nods esclavos esten registrados en el repgmr
su - postgres

psql

SELECT * FROM pg_stat_replication
```
## 9 Replica el nodo Master en cada nodo Esclavo
```bash
# Ingresa en el usuario postgres de cada nodo esclavo
su - postgres

repmgr -f /etc/repmgr.conf standby register

# Tiene que salir el siguiente mensaje 
# 
# INFO: standby registration complete
# NOTICE: standby node "pg2" (ID: 2) successfully registered

# Verifica en el repmgre que se haya regisrado correctamente
repmgr -f /etc/repmgr.conf cluster show
```
## 10 Registra cada nodo, incluyendo al master y los esclavos, en el repmgrd
```bash
# Comando
repmgrd -f /etc/repmgr.conf -d
```
