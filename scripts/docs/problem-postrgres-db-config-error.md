# postrgres db config

in `docker-compose.prod.yml` file

```yaml
  db:
    image: postgres:12.0-alpine
    volumes:
      - $HOME/midata/private/postgres_data2:/var/lib/postgresql/data/
    env_file:
      - ./.env.db.prod
```

Error message when starting fresh with new persistent storage volumes in `~/midata/private/`

```bash
db_1     | Error: Database is uninitialized and superuser password is not specified.
db_1     |        You must specify POSTGRES_PASSWORD to a non-empty value for the
db_1     |        superuser. For example, "-e POSTGRES_PASSWORD=password" on "docker run".
db_1     |
db_1     |        You may also use "POSTGRES_HOST_AUTH_METHOD=trust" to allow all
db_1     |        connections without a password. This is *not* recommended.
db_1     |
db_1     |        See PostgreSQL documentation about "trust":
db_1     |        https://www.postgresql.org/docs/current/auth-trust.html
```

in `.env.prod` file

The Django variable names for DB credentials are generic.

```bash
SQL_USER=qaryapp_db_user
SQL_PASSWORD=qaryapp_db_password_changeme
SQL_DATABASE=qaryapp_db_name
```

entire `.env.prod.db` file

Notice the environment variable names are different from Django and .env.prod but the values must be consistent!

```bash
POSTGRES_USER=qaryapp_db_user
POSTGRES_PASSWORD=qaryapp_db_password_changeme
POSTGRES_DB=qaryapp_db_name
```


