# Tutorial 06 - El Primer Estrangulamiento (Strangler Pattern)

Arquitectura de Software 2026 - EAFIT
Jeronimo Carvajal Zuluaga

Continuacion del Tutorial 05. Siguiendo el **Strangler Pattern**, se extrae la funcionalidad de compra del monolito Django a un microservicio ligero en **Flask**. Nginx decide a quien mandar cada peticion segun la version de la API, y el usuario no nota el cambio.

```
                         ┌── /api/v1/...      ──► web_django  (Monolito v1, Gunicorn :8000) ──► db (PostgreSQL)
Internet ──► Nginx :80 ──┤
                         └── /api/v2/comprar  ──► pagos_flask (Microservicio v2, Gunicorn :5000)
```

## Que se agrego / cambio

| Archivo | Cambio |
|---|---|
| `microservicio_pagos/app.py` | Microservicio Flask con `POST /api/v2/comprar` |
| `microservicio_pagos/Dockerfile` | Imagen de Flask + Gunicorn (python:3.11-alpine) |
| `docker-compose.yml` | El servicio `web` pasa a llamarse `web_django`; nuevo servicio `pagos_flask` |
| `nginx/nginx.conf` | Dos upstreams (`django_v1` y `flask_v2`) y el ruteo por version |
| `tienda_app/api/views.py`, `urls.py` | Nuevo `GET /api/v1/productos/` (lista de libros, sigue en Django) |

Adicional al PDF:
- El log de Nginx usa un formato propio que muestra `backend=django_v1` o `backend=flask_v2` en cada peticion, para ver el enrutamiento con `docker compose logs nginx`.
- Se deja `location /` hacia Django para que el resto del monolito (inventario, estaticos) siga funcionando.

## Endpoints

| Metodo | Ruta | Quien responde |
|---|---|---|
| GET | `/api/v1/productos/` | Django (v1) |
| POST | `/api/v1/comprar/` | Django (v1) |
| POST | `/api/v2/comprar` body `{"producto_id": 1, "cantidad": 2}` | Flask (v2) |

## Despliegue en EC2

```
git clone https://github.com/Jerocz/tutorial06-Strangler-Flask.git
cd tutorial06-Strangler-Flask
docker compose up -d --build
docker compose logs nginx
```
