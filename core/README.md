## Use PostgreSQL in docker

#### Initial steps

Firstly, you have to install **Docker** on your system.

Then, you can run command below:
```bash
sudo docker run -d --rm --name smart_parking_db -p 5555:5432 -e POSTGRES_USER=smart_parking_user -e POSTGRES_PASSWORD=password -e POSTGRES_DB=smart_parking postgres:13
```
*NOTE: if you are running Windows then run commands without `sudo`*

The command above will set up clean PostgreSQL with no data in it each time you run it - good for testing.

#### Add persistence to database

If you want to save data between your DB reloads then firtsly create new Docker volume:

```bash
sudo docker volume create smart_parking_volume
```

After this run updated version of `docker run` command:
```bash
sudo docker run -d --rm --name smart_parking_db -v smart_parking_volume:/var/lib/postgresql/data -p 5555:5432 -e POSTGRES_USER=smart_parking_user -e POSTGRES_PASSWORD=password -e POSTGRES_DB=smart_parking postgres:13
```

#### Stop database

To stop Docker container just type this:
```bash
sudo docker stop smart_parking_db
```

#### Update Django with new DB

Create `.env` file in this directory if you haven't done it before. Then add these lines to it:
```
DB_NAME=smart_parking
DB_USER=smart_parking_user
DB_PASSWORD=password
DB_PORT=5555
```
