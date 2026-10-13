# Tutorial 05 - El Escudo Arquitectonico (Nginx + Gunicorn)

Arquitectura de Software 2026 - EAFIT
Jeronimo Carvajal Zuluaga

Continuacion del Tutorial 04. Se deja de usar `runserver` y se arma una arquitectura de produccion de tres capas:

```
Internet ──► Nginx (puerto 80) ──► Gunicorn + Django (web:8000, red interna) ──► PostgreSQL (db)
```

- **Nginx** es el proxy inverso: es el unico contenedor que expone un puerto al exterior (80).
- **Gunicorn** es el servidor WSGI que ejecuta Django (reemplaza a `runserver`).
- **Django ya no expone el puerto 8000**: solo Nginx puede hablar con el dentro de la red de Docker.

Esta es la base para el Strangler Pattern del Tutorial 06: Nginx podra mandar algunas rutas a otro servicio.

## Que se agrego / cambio

| Archivo | Cambio |
|---|---|
| `requirements.txt` | Se agrega `gunicorn` |
| `nginx/nginx.conf` | Configuracion del proxy inverso (upstream `web:8000`) |
| `docker-compose.yml` | `web` usa Gunicorn y ya no tiene `ports`; nuevo servicio `nginx` en el puerto 80 |
| `Tienda/settings.py` | `STATIC_ROOT` para `collectstatic` |

Adicional al PDF: como Gunicorn no sirve archivos estaticos, se corre `collectstatic` al arrancar y Nginx entrega `/static/` desde un volumen compartido (`static_volume`). Sin esto la pagina de DRF se ve sin estilos.

## Despliegue en EC2

```
git clone https://github.com/Jerocz/tutorial05-Nginx-Gunicorn.git
cd tutorial05-Nginx-Gunicorn
docker compose up -d --build
docker ps
```

- API: `http://<IP-EC2>/api/v1/comprar/` (sin puerto)
- `http://<IP-EC2>:8000` ya no responde
