### Features

# FastApi-PostgreSQL-API

API FastApi &lt;> PostgreSQL

Configuración:
+ Usar este Template de github o clonar repositorio.
+ Ingresar a la carpeta creada.
+ Crear entorno virtual
    + python -m venv c:\ruta\al\entorno\virtual
+ Activar entorno virtual
    + cd scripts
    + activate
+ Instalar librerias
    + sudo apt-get install libpq-dev 
    + pip install -r .\requirements.txt
+ Configurar variable de entorno
    + renombrar "\_.env" a ".env" o crear un nuevo archivo ".env", y completarlo con las variables de entorno.
+ Iniciar
    + uvicorn app:app --reload
