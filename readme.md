# R-D-A-L REST

Backend hecho en django con la finalidad de manejar la logica del servidor del proyecto r-d-a-l.

## Instalación del entorno de desarrollo

### Requisitos:

- Tener python instalado ( Python 3.13.11 )

1. Primero ejecutar el comando  ` python -m venv venv ` para crear el entorno virtual
2. Activar el venv con  ` venv/Scripts/activate  `
3. Ejecutar ` pip install -r requirements.txt ` para instalar las dependencias.
4. Crear una base de datos sqlite llamada ` db.sqlite3 ` para la base de datos de desarrollo
5. Ejecutar el comando ` python manage.py migrate ` para crear las tablas en la base de datos creada.
6. Crear un superusuario para el desarrollo con ` python manage.py createsuperuser ` y colocar las credenciales que sean

## Migrar base de datos a PostgreSQL

### Requisitos:

- Tener Docker instalado en tu maquina.

1. ejecutar en la terminal ` docker-compose up -d `. Esto levantara una base de datos PostgreSQL y repetir los mismos pasos para migrar

### Creacion de variables de entorno

es importante crear un archivo llamado .env el cual contenga los siguientes valores:
- DB_USER
- DB_PASSWORD
- DB_NAME
- SECRET_KEY
- DEBUG
- DB_HOST
- DB_PORT

Ademas antes de utilizar el frontend leer ` notes.txt `

