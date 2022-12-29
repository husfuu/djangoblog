## Docker Postgres
    ```shell
    docker run --rm \
    --name djangoblog \
    -e POSTGRES_DB=djangoblog_db  \
    -e POSTGRES_USER=learn \
    -e POSTGRES_PASSWORD=mysecretpassword \
    -e PGDATA=/var/lib/postgresql/data/pgdata \
    -v "$PWD/djangoblog-data:/var/lib/postgresql/data" \
    -p 5432:5432 \
    postgres:13
    ```

- access postgres CLI
    ```
    >>> sudo docker exec -it djangoblog bash
    
    >>> psql -h 127.0.0.1 -U learn djangoblog_db
    ```