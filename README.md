<div align="center">
<h1 align="center">Dockerized-Django-PostgreSQL-Minio</h1>
<h3 align="center">Sample Project to use django plus minio file storage app</h3>
</div>
<p align="center">
<a href="https://www.python.org" target="_blank"> <img src="https://github.com/tandpfun/skill-icons/blob/main/icons/Python-Dark.svg" alt="python" width="40" height="40"/> </a>
<a href="https://www.djangoproject.com/" target="_blank"> <img src="https://github.com/tandpfun/skill-icons/blob/main/icons/Django.svg" alt="django" width="60" height="40"/> </a> 
<a href="https://www.docker.com/" target="_blank"> <img src="https://github.com/tandpfun/skill-icons/blob/main/icons/Docker.svg" alt="docker" width="40" height="40"/> </a>
<a href="https://www.postgresql.org" target="_blank"> <img src="https://github.com/tandpfun/skill-icons/blob/main/icons/PostgreSQL-Dark.svg" alt="postgresql" width="40" height="40"/> </a>
<a href="https://www.nginx.com" target="_blank"> <img src="https://github.com/tandpfun/skill-icons/blob/main/icons/Nginx.svg" alt="nginx" width="40" height="40"/> </a>
<a href="https://git-scm.com/" target="_blank"> <img src="https://github.com/tandpfun/skill-icons/blob/main/icons/Git.svg" alt="git" width="40" height="40"/> </a>
<a href="https://minio.io/" target="_blank"> <img src="https://brandfetch.com/minio.io?view=library&library=default&collection=logos&asset=idAq3Bu8sr&utm_source=https%253A%252F%252Fbrandfetch.com%252Fminio.io&utm_medium=copyAction&utm_campaign=brandPageReferral" alt="git" width="100" height="40"/> </a>
</p>
![id7hrSLNkH_1741508525597](https://github.com/user-attachments/assets/ce829202-0b4c-42d9-bd1d-1a5e1e9285f9)

# Guideline
- [Guideline](#guideline)
- [Goal](#goal)
- [Development usage](#development-usage)
  - [Clone the repo](#clone-the-repo)
  - [Enviroment Varibales](#enviroment-varibales)
  - [Build everything](#build-everything)
  - [Note](#note)
- [Testing Usage](#testing-usage)
  - [running all tests](#running-all-tests)

# Goal
This project main goal is to provide a simple way to deploy a django project into hamravesh service provider.

# Development usage
You'll need to have [Docker installed](https://docs.docker.com/get-docker/).
It's available on Windows, macOS and most distros of Linux. 

If you're using Windows, it will be expected that you're following along inside
of [WSL or WSL
2](https://nickjanetakis.com/blog/a-linux-dev-environment-on-windows-with-wsl-2-docker-desktop-and-more).

That's because we're going to be running shell commands. You can always modify
these commands for PowerShell if you want.


## Clone the repo
Clone this repo anywhere you want and move into the directory:
```bash
git clone https://github.com/MhmdRdbri/Dockerized-Django-PostgreSQL-Minio.git
```

## Enviroment Varibales
enviroment varibales are included in docker-compose.yml file for debugging mode and you are free to change commands inside:

```yaml
services:
  backend:
  command: sh -c "python manage.py check_database && \ 
                      python manage.py collectstatic --noinput && \
                      yes | python manage.py makemigrations  && \
                      yes | python manage.py migrate  && \                    
                      python manage.py runserver 0.0.0.0:8000"
    environment:      
      - DEBUG=True
```
Note: in order for minio to work properly and serve files as statics you have to collect the statics of the project.

also you can edit your minio service configurations inside the docker-compose.yml file:
```yaml
  minio:
    image: minio/minio
    container_name: minio
    expose:
      - 9000
      - 9001
    ports:
      - "9000:9000"
      - "9001:9001"
    volumes:
      - './minio/data:/data'
    environment:
      MINIO_ROOT_USER: minioadmin
      MINIO_ROOT_PASSWORD: minioadmin
    command: server --console-address ":9001" /data

```

## Build everything

The first time you run this it's going to take 5-10 minutes depending on your
internet connection speed and computer's hardware specs. That's because it's
going to download a few Docker images such as minio and build the Python + requirements dependencies. and dont forget to create a .env file inside dev folder for django and postgres with the samples.

```bash
docker compose up --build
```

Now that everything is built and running we can treat it like any other Django
app.

## Note

If you receive an error about a port being in use? Chances are it's because
something on your machine is already running on port 8000. then you have to change the docker-compose.yml file according to your needs.

also 
feel free to change the default configurations provided inside settings.py:
```python
# Minio storage
## global config
DEFAULT_FILE_STORAGE = "minio_storage.storage.MinioMediaStorage"
STATICFILES_STORAGE = "minio_storage.storage.MinioStaticStorage"
MINIO_STORAGE_ENDPOINT = config('MINIO_STORAGE_ENDPOINT', default="minio:9000")
MINIO_EXTERNAL_STORAGE_ENDPOINT= config('MINIO_EXTERNAL_STORAGE_ENDPOINT', default="http://127.0.0.1:9000")

## security configs
MINIO_STORAGE_ACCESS_KEY = config('MINIO_STORAGE_ACCESS_KEY', default="minioadmin")
MINIO_STORAGE_SECRET_KEY = config('MINIO_STORAGE_SECRET_KEY', default="minioadmin")
MINIO_STORAGE_USE_HTTPS = config('MINIO_STORAGE_USE_HTTPS',cast=bool, default="False")

## static files config
MINIO_STORAGE_MEDIA_BUCKET_NAME = config('MINIO_STORAGE_MEDIA_BUCKET_NAME',default='media')
MINIO_STORAGE_MEDIA_USE_PRESIGNED = True
MINIO_STORAGE_AUTO_CREATE_MEDIA_BUCKET = True

## media files config
MINIO_STORAGE_STATIC_BUCKET_NAME = config('MINIO_STORAGE_STATIC_BUCKET_NAME',default='static')
MINIO_STORAGE_STATIC_USE_PRESIGNED = True
MINIO_STORAGE_AUTO_CREATE_STATIC_BUCKET = True

# changing base url schema for static and media serve
# by default in dev mode it will look for localhost port 9000 you can configure another when using online

MINIO_STORAGE_STATIC_URL = config('MINIO_STORAGE_STATIC_URL',f'{MINIO_EXTERNAL_STORAGE_ENDPOINT}/{MINIO_STORAGE_STATIC_BUCKET_NAME}')
MINIO_STORAGE_MEDIA_URL = config('MINIO_STORAGE_MEDIA_URL',f'{MINIO_EXTERNAL_STORAGE_ENDPOINT}/{MINIO_STORAGE_MEDIA_BUCKET_NAME}')

```

# Testing Usage
## running all tests
```bash
docker compose run --rm backend sh -c " black -l 79 && flake8 && python manage.py test" -v core:/app
```
or
```bash
docker compose exec backend sh -c sh -c " black -l 79 && flake8 && python manage.py test" 
```
