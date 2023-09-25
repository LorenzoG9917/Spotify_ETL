# Proyecto Spotify Data

## Objetivo
Este proyecto tiene como objetivo obtener datos de las canciones reproducidas en las últimas 24 horas en Spotify y cargar estos datos en una base de datos PostgreSQL. Utiliza Flask para autorizar la aplicación con Spotify y Python para interactuar con la API de Spotify y la base de datos.

## Arquitectura

## Requisitos del Sistema
Asegúrate de tener instalado lo siguiente:
- Python 3.x
- PostgreSQL

## Instrucciones de Uso

A continuación, se detallan los pasos para ejecutar la aplicación:

### Paso 1: Clonar el Repositorio

Clona este repositorio en tu máquina local utilizando el siguiente comando:

```bash
git clone <URL_del_repositorio>
```
### Paso 2: Instalar Dependencias
```bash
pip install -r requirements.txt
```
### Paso 3: Configuración
- Abre el archivo flask_server.py y proporciona tu Client ID de Spotify en la variable client_id. Este servidor Flask se utiliza para obtener el token de acceso de Spotify.

### Paso 4: Ejecutar el Servidor Flask
```bash
python flask_server.py
```
Esto abrirá automáticamente una ventana del navegador para autorizar la aplicación en Spotify(debes inicar sesión con tu cuenta de Spotifiy). El token de acceso se guardará en un archivo llamado access_token.txt.

###  Paso 5: Obtener y Cargar los Datos

Ejecuta el script spotify_api.py. Este script obtendrá datos de las canciones reproducidas en las últimas 24 horas utilizando el token de acceso. Los datos se procesarán y se almacenarán en una base de datos PostgreSQL.

### Paso 6: Verificar la Base de Datos
Puedes verificar la base de datos para asegurarte de que los datos se hayan cargado correctamente.

## Agradecimientos

- Agradecimientos especiales a [Karolina Sowinska](https://www.linkedin.com/in/karolina-sowinska-b3070b103/) por la creación de este proyecto con fines educativos.

## Autor
Este proyecto ha sido desarrollado por [Lorenzo Guerrero](https://www.linkedin.com/in/lorenzoguerrero17/) con fines educativos.