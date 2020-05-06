## Problem 0

Turn off laptop screen on headless Ubuntu server (no gnome).

Log in as root on the laptop physical keyboard.

```
# change: HandleLidSwitch=suspend
# to:     HandleLidSwitch=ignore
nano /etc/systemd/logind.conf
setterm --powersave powerdown
shutdown -r now
```

Then wait a few seconds. After screen times out (but backlight still on) you can close the lid.

Other people (with a Desktop like Gnome?) had to `nano /etc/Upower/UPower.conf` and set `IgnoreLid=false`.

## Problem 1

Can't connect to Elastic Search on totalgood.org

chown and chmod fixed it


## Problem 2 Postgres

After rebuilding a fresh install on more recent branch, with chown and chmod 775 in build.sh,

manage.py migrate fails because postgres database not reachable

```bash
albert-large-v2-0.2.0.zip: 33.1MB [00:19, 1.73MB/s]
Traceback (most recent call last):
  File "/home/app/.local/lib/python3.7/site-packages/django/db/backends/base/base.py", line 217, in ensure_connection
    self.connect()
  File "/home/app/.local/lib/python3.7/site-packages/django/db/backends/base/base.py", line 195, in connect
    self.connection = self.get_new_connection(conn_params)
  File "/home/app/.local/lib/python3.7/site-packages/django/db/backends/postgresql/base.py", line 178, in get_new_connection
    connection = Database.connect(**conn_params)
  File "/home/app/.local/lib/python3.7/site-packages/psycopg2/__init__.py", line 127, in connect
    conn = _connect(dsn, connection_factory=connection_factory, **kwasync)
psycopg2.OperationalError: FATAL:  database "django_qary_prod_db" does not exist


The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "manage.py", line 21, in <module>
    main()
  File "manage.py", line 17, in main
    execute_from_command_line(sys.argv)
  File "/home/app/.local/lib/python3.7/site-packages/django/core/management/__init__.py", line 381, in execute_from_command_line
    utility.execute()
  File "/home/app/.local/lib/python3.7/site-packages/django/core/management/__init__.py", line 375, in execute
    self.fetch_command(subcommand).run_from_argv(self.argv)
  File "/home/app/.local/lib/python3.7/site-packages/django/core/management/base.py", line 323, in run_from_argv
    self.execute(*args, **cmd_options)
  File "/home/app/.local/lib/python3.7/site-packages/django/core/management/base.py", line 364, in execute
    output = self.handle(*args, **options)
  File "/home/app/.local/lib/python3.7/site-packages/django/core/management/base.py", line 83, in wrapped
    res = handle_func(*args, **kwargs)
  File "/home/app/.local/lib/python3.7/site-packages/django/core/management/commands/migrate.py", line 87, in handle
    executor = MigrationExecutor(connection, self.migration_progress_callback)
  File "/home/app/.local/lib/python3.7/site-packages/django/db/migrations/executor.py", line 18, in __init__
    self.loader = MigrationLoader(self.connection)
  File "/home/app/.local/lib/python3.7/site-packages/django/db/migrations/loader.py", line 49, in __init__
    self.build_graph()
  File "/home/app/.local/lib/python3.7/site-packages/django/db/migrations/loader.py", line 212, in build_graph
    self.applied_migrations = recorder.applied_migrations()
  File "/home/app/.local/lib/python3.7/site-packages/django/db/migrations/recorder.py", line 73, in applied_migrations
    if self.has_table():
  File "/home/app/.local/lib/python3.7/site-packages/django/db/migrations/recorder.py", line 56, in has_table
    return self.Migration._meta.db_table in self.connection.introspection.table_names(self.connection.cursor())
  File "/home/app/.local/lib/python3.7/site-packages/django/db/backends/base/base.py", line 256, in cursor
    return self._cursor()
  File "/home/app/.local/lib/python3.7/site-packages/django/db/backends/base/base.py", line 233, in _cursor
    self.ensure_connection()
  File "/home/app/.local/lib/python3.7/site-packages/django/db/backends/base/base.py", line 217, in ensure_connection
    self.connect()
  File "/home/app/.local/lib/python3.7/site-packages/django/db/utils.py", line 89, in __exit__
    raise dj_exc_value.with_traceback(traceback) from exc_value
  File "/home/app/.local/lib/python3.7/site-packages/django/db/backends/base/base.py", line 217, in ensure_connection
    self.connect()
  File "/home/app/.local/lib/python3.7/site-packages/django/db/backends/base/base.py", line 195, in connect
    self.connection = self.get_new_connection(conn_params)
  File "/home/app/.local/lib/python3.7/site-packages/django/db/backends/postgresql/base.py", line 178, in get_new_connection
    connection = Database.connect(**conn_params)
  File "/home/app/.local/lib/python3.7/site-packages/psycopg2/__init__.py", line 127, in connect
    conn = _connect(dsn, connection_factory=connection_factory, **kwasync)
django.db.utils.OperationalError: FATAL:  database "django_qary_prod_db" does not exist
```

After rebuilding containers and chown on elastic search volume ownership changes back:

```bash
{'sqlite': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': '/home/app/web/db.sqlite3'}, 'postgres': {'ENGINE': 'django.db.backends.postgresql', 'NAME': 'django_qary_prod_db', 'USER': 'django_qary_prod_dbun', 'PASSWORD': 'django_qary_prod_pa
ss_1027', 'HOST': 'db', 'PORT': '5432'}, 'default': {'ENGINE': 'django.db.backends.postgresql', 'NAME': 'django_qary_prod_db', 'USER': 'django_qary_prod_dbun', 'PASSWORD': 'django_qary_prod_pass_1027', 'HOST': 'db', 'PORT': '5432'}}

0 static files copied to '/home/app/web/staticfiles', 157 unmodified.
root@tangible-notebook:~/django-qary# ls -al /midata/private/esdata/nodes/0/_state
total 44
drwxrwxr-- 2 root     docker  4096 May  5 22:43 .
drwxrwxr-- 3 root     docker  4096 May  5 22:42 ..
-rw-rw-r-- 1 tangible root     225 May  5 22:43 _11.cfe
-rw-rw-r-- 1 tangible root   12979 May  5 22:43 _11.cfs
-rw-rw-r-- 1 tangible root     370 May  5 22:43 _11.si
-rw-rw-r-- 1 tangible root     109 May  5 22:43 manifest-8.st
-rw-rw-r-- 1 tangible root      89 May  5 22:43 node-8.st
-rw-rw-r-- 1 tangible root     232 May  5 22:43 segments_1t
-rwxrwxr-- 1 root     docker     0 May  4 22:04 write.lock

root@tangible-notebook:~/django-qary# ls -al /midata/private/postgres_data/
total 132
drwx------ 19   70 root    4096 May  5 22:42 .
drwxrwxr--  6 root docker  4096 May  5 22:22 ..
drwxrwxr--  6   70     70  4096 May  5 22:22 base
drwxrwxr--  2   70     70  4096 May  5 22:43 global
drwxrwxr--  2   70     70  4096 May  5 22:22 pg_commit_ts
drwxrwxr--  2   70     70  4096 May  5 22:22 pg_dynshmem
-rwxrwxr--  1   70     70  4535 May  5 22:22 pg_hba.conf
-rwxrwxr--  1   70     70  1636 May  5 22:22 pg_ident.conf
```
