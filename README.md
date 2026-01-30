# PRACTICA-EXAMEN Despliegue de Aplicaciones Web - CURSO DAW2
Despliegue de FastAPI en VPS (Debian 13) con NGINX y HTTPS
Esta practica-examen  asume que : 

tienes funcionando en Docker tu aplicacion FastAPI (Zapatillas, por ejemplo)
acceso al servidor via sFTP y un administrador del sistema como Jordi ;-) (risas)
 ya tienes  tu código subido al servidor, un dominio (DNS)  y acceso  sudo.

TIP: tienes funcionando en WSL  tu aplicacion FastAPI (Zapatillas, por ejemplo), antes de pasar de desarrollo a produccion (en nuestro servidor de pruebas ‘zzz’)
1. Configurar el DNS (tarea a realizar por fenix)
(Igual que tu versión original, esto es independiente del sistema operativo)
En tu proveedor de dominios, crea un Registro A.
Apunta ejemplo.com a la IP de tu VPS (ej: 123.123.123.123).
(Opcional) Crea un CNAME para www apuntando a ejemplo.com.

2. Actualizar el VPS (o tu Windows Subsytem for Linux)
Prepara el sistema Debian en tu WSL:


sudo apt update && sudo apt upgrade -y
sudo apt install nginx 

( Python viene pre-instalado por defecto, en Debian )


3. Python y Configurar la App

Crear el entorno virtual:
Bash
cd /ruta/a/tu/proyecto
python3 -m venv env
source env/bin/activate


Instalar librerías Python:
Asegúrate de que tu requirements.txt incluya fastapi, uvicorn y gunicorn. Si no, instálalos:
Bash
pip install -r requirements.txt
pip install gunicorn uvicorn


Configurar Gunicorn (Systemd Service):
Creamos un servicio para que la app arranque sola y se reinicie si falla.
Bash
sudo nano /etc/systemd/system/zapatillas.service

Contenido corregido:
Se añade -k uvicorn.workers.UvicornWorker (Vital para FastAPI).
Se cambia el bind a 127.0.0.1 (Por seguridad, para que no sea accesible desde fuera sin pasar por NGINX).
Ini, TOML
[Unit]
Description=Gunicorn instance to serve ZapatillasFastAPI
After=network.target

[Service]
User=tu_usuario
Group=www-data
WorkingDirectory=/ruta/a/tu/proyecto
Environment="PATH=/ruta/a/tu/proyecto/env/bin"
# OJO: Cambia 'app:app' por 'nombre_archivo:nombre_instancia_fastapi'
ExecStart=/ruta/a/tu/proyecto/env/bin/gunicorn -k uvicorn.workers.UvicornWorker --workers 4 --bind 127.0.0.1:8000 app:app

[Install]
WantedBy=multi-user.target


Arrancar la aplicación:
Bash
sudo systemctl daemon-reload
sudo systemctl start zapatillas
sudo systemctl enable zapatillas


4. Configurar NGINX (Fase HTTP)
Primero configuramos NGINX solo para HTTP (Puerto ¿XY?). 

Configurar el servidor Web NGINX:



Crear archivo de configuración:
Bash
sudo nano /etc/nginx/sites-available/zapatillas

Contenido inicial:
Nginx
server {
    listen ¿XY?;
    server_name ¿ejemplo.com? ¿www.ejemplo.com?;

    location / {
        proxy_pass … ¿?    }
}
Te has preguntado, en la configuracion de Nginx, … ¿Que directivas proxy son necesarias ?
Activar el sitio y verificar:
Bash
sudo ln -s /etc/nginx/sites-available/zapatillas /etc/nginx/sites-enabled
# Verificar que la sintaxis es correcta
sudo nginx -t
# Reiniciar
sudo systemctl restart nginx

En este punto, tu web ya debería funcionar por http://ejemplo.com.


4. Configurar NGINX (Fase HTTP)

En este punto, tu web ya debería funcionar por https://ejemplo.com.

NOTAS:
Dependencias: Se añadió python3-venv (necesario en Debian).
Gunicorn: Se configura el worker uvicorn (necesario para FastAPI)

