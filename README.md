# ZapatillasFastAPI

API REST para gestionar un catalogo de zapatillas.

## Requisitos

- Python 3.11+

## Instalacion Local

```bash
# Clonar repositorio
git clone <url-repo>
cd ZapatillasFastAPI

# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar
uvicorn src.main:app --reload
```

La base de datos SQLite se crea automaticamente en `zapatillas.db`.

## Despliegue en Produccion (Debian/Ubuntu)

### 1. Preparar el servidor

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install python3 python3-venv python3-pip nginx -y
```

### 2. Configurar la aplicacion

```bash
cd /var/www
sudo git clone <url-repo> zapatillas
cd zapatillas

sudo python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Crear servicio systemd

```bash
sudo nano /etc/systemd/system/zapatillas.service
```

```ini
[Unit]
Description=Zapatillas FastAPI
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/zapatillas
Environment="PATH=/var/www/zapatillas/venv/bin"
ExecStart=/var/www/zapatillas/venv/bin/gunicorn -k uvicorn.workers.UvicornWorker -w 4 -b 127.0.0.1:8000 src.main:app

[Install]
WantedBy=multi-user.target
```

```bash
sudo chown -R www-data:www-data /var/www/zapatillas
sudo systemctl daemon-reload
sudo systemctl start zapatillas
sudo systemctl enable zapatillas
```

### 4. Configurar NGINX

```bash
sudo nano /etc/nginx/sites-available/zapatillas
```

```nginx
server {
    listen 80;
    server_name tu-dominio.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/zapatillas /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 5. SSL con Certbot (opcional)

```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d tu-dominio.com
```

## Endpoints

| Metodo | Ruta | Descripcion |
|--------|------|-------------|
| GET | /zapatillas | Lista todas |
| POST | /zapatillas | Crear nueva |
| GET | /zapatillas/{id} | Obtener por ID |
| PATCH | /zapatillas/{id} | Actualizar |
| DELETE | /zapatillas/{id} | Eliminar |
| GET | /docs | Swagger UI |
| GET | /redoc | ReDoc |

## Estructura

```
.
├── src/
│   ├── main.py              # Aplicacion FastAPI
│   ├── models/              # Modelos SQLModel
│   ├── data/                # Repositorio y DB
│   ├── routers/             # Endpoints API
│   ├── templates/           # Plantillas Jinja2
│   └── static/              # Archivos estaticos
├── requirements.txt
├── zapatillas.db            # Base de datos SQLite (auto-generada)
└── README.md
```

---

## Propuestas de Mejora KISS

### Aplicadas en esta version

| Antes | Ahora | Beneficio |
|-------|-------|-----------|
| MySQL (servidor externo) | SQLite (archivo local) | Zero configuracion, sin dependencias externas |
| 9 dependencias | 6 dependencias | Menos superficie de ataque, instalacion mas rapida |
| .env con 5 variables | .env con 1 variable (opcional) | Configuracion minima |
| Requiere instalar MySQL | Solo Python | Despliegue inmediato |

### Futuras mejoras posibles

1. **Eliminar Jinja2/templates** si solo se usa como API REST pura
2. **Eliminar python-multipart** si no se necesitan uploads de archivos
3. **Un solo archivo** - consolidar todo en `main.py` para proyectos pequenos
4. **Usar SQLite en memoria** para testing: `DATABASE_PATH=:memory:`
5. **Eliminar routers/** si hay pocos endpoints - definirlos directamente en main.py

### Principios KISS aplicados

- **Sin Docker**: Python + venv es suficiente
- **Sin MySQL**: SQLite viene incluido en Python
- **Sin .env obligatorio**: valores por defecto sensatos
- **Sin configuracion**: funciona al instalar dependencias
- **Datos de ejemplo**: la app arranca lista para probar
