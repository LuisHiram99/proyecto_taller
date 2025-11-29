# Backend - Taller Management System

Este es el backend del sistema de gestión para talleres. Proporciona una API REST construida con FastAPI y PostgreSQL.

## Requisitos Previos

### Con Docker (Recomendado)

- Docker
- Docker Compose

### Sin Docker

- Python 3.8 o superior
- PostgreSQL 12 o superior
- pip (gestor de paquetes de Python)

## Inicio Rápido con Docker

La forma más sencilla de ejecutar el proyecto es usando Docker Compose, que configura automáticamente tanto la API como la base de datos PostgreSQL.

### 1. Construir y ejecutar los contenedores

```bash
# Desde el directorio backend
docker-compose up --build
```

Este comando:

- Construye la imagen Docker de la API
- Descarga la imagen de PostgreSQL 17
- Crea y configura la base de datos
- Ejecuta las migraciones automáticamente
- Inicia el servidor en http://localhost:8000

### 2. Comandos útiles de Docker

```bash
# Ejecutar en segundo plano (detached mode)
docker-compose up -d

# Ver logs de los contenedores
docker-compose logs -f

# Ver logs solo de la API
docker-compose logs -f api

# Ver logs solo de la base de datos
docker-compose logs -f db

# Detener los contenedores
docker-compose down

# Detener y eliminar volúmenes (borra la base de datos)
docker-compose down -v

# Reconstruir las imágenes
docker-compose build --no-cache

# Reiniciar un servicio específico
docker-compose restart api
docker-compose restart db
```

### 3. Acceder a la base de datos PostgreSQL

```bash
# Conectarse al contenedor de la base de datos
docker-compose exec db psql -U luishernandez -d talleres_db

# O desde tu máquina local (si tienes psql instalado)
psql -h localhost -p 5435 -U luishernandez -d talleres_db
# Contraseña: 1234
```

### 4. Ejecutar comandos dentro del contenedor de la API

```bash
# Abrir un shell interactivo en el contenedor
docker-compose exec api sh

# Ejecutar migraciones manualmente
docker-compose exec api alembic upgrade head

# Crear una nueva migración
docker-compose exec api alembic revision --autogenerate -m "descripción del cambio"

# Ver el estado de las migraciones
docker-compose exec api alembic current
```

### 5. Configuración del entorno Docker

El archivo `docker-compose.yaml` configura:

- **API**: Puerto 8000, con recarga automática en desarrollo
- **Base de datos**: PostgreSQL 17 en puerto 5435 (para evitar conflictos con instalaciones locales)
- **Volúmenes**: Persistencia de datos en `postgres_data`
- **Variables de entorno**: Cargadas desde `./config/.env`

### 6. Desarrollo con Docker

Los archivos en `./src` están montados como volumen, lo que significa que los cambios en el código se reflejan automáticamente sin necesidad de reconstruir el contenedor.

---

## Configuración Manual (Sin Docker)

Si prefieres ejecutar el proyecto sin Docker, sigue estos pasos:

### 1. Crear un entorno virtual:

```bash
# Crear el entorno virtual
python -m venv venv

# Activar el entorno virtual
# En macOS/Linux:
source venv/bin/activate
# En Windows:
# .\venv\Scripts\activate
```

2. Instalar dependencias:

```bash
# Navegar al directorio backend
cd backend

# Instalar requerimientos
pip install -r requirements.txt
```

### 2. Configuración de la Base de Datos

1. Crear la base de datos en PostgreSQL:

```bash
# Conectar a PostgreSQL
psql -U postgres

# Crear la base de datos
CREATE DATABASE taller_db;
```

2. Configurar las variables de entorno:

   - Copiar el archivo de ejemplo `.env.example` a `.env`:

   ```bash
   cd backend/src
   cp .env.example .env
   ```

   - Editar el archivo `.env` con tus credenciales:

   ```env
   DB_USER=tu_usuario
   DB_PASSWORD=tu_contraseña
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=taller_db
   ```

   Nota: El archivo `.env` está incluido en `.gitignore` para evitar exponer credenciales sensibles.

3. Crear las tablas y tipos necesarios con alembic:

```bash
# Desde el directorio del backend correr lo siguiente:
alembic upgrade head

```

- Nota: Esto aplica todas las migraciones de la base de datos

### 3. Ejecutar el Servidor

```bash
# Ejecutar el servidor con recarga automática
uvicorn main:app --reload
```

El servidor estará disponible en: http://localhost:8000

## Endpoints Disponibles

### Usuarios

- `POST /api/v1/usuarios/` - Crear usuario
- `GET /api/v1/usuarios/` - Listar usuarios
- `GET /api/v1/usuarios/{id}` - Obtener usuario por ID
- `PUT /api/v1/usuarios/{id}` - Actualizar usuario
- `DELETE /api/v1/usuarios/{id}` - Eliminar usuario

### Documentación API

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Ejemplo de Uso

1. Crear un nuevo usuario:

```bash
curl -X POST "http://localhost:8000/api/v1/usuarios/" \
     -H "Content-Type: application/json" \
     -d '{
       "nombre": "Juan",
       "apellido": "Pérez",
       "rol": "gerente",
       "acronimo": "JP"
     }'
```

2. Listar usuarios:

```bash
curl "http://localhost:8000/api/v1/usuarios/"
```

## Estructura del Proyecto

```
backend/
├── requirements.txt
├── alembic               # Migraciones de la base de datos
├── config                # Configuración de las variables
├── src/
│   ├── main.py           # Punto de entrada de la aplicación
│   ├── db/
│   │   ├── database.py   # Configuración de la base de datos
│   │   ├── models.py     # Modelos SQLAlchemy
│   │   ├── schemas.py    # Esquemas Pydantic
│   │   └── schema/       # Scripts SQL
│   └── handler/
│       └── usuarios.py    # Manejadores de endpoints
```

## Solución de Problemas Comunes

1. Error de conexión a la base de datos:

   - Verificar que PostgreSQL esté corriendo
   - Confirmar credenciales en DATABASE_URL
   - Verificar que la base de datos exista

2. Error 422 en requests:

   - Verificar el formato JSON del body
   - Confirmar que los valores de rol sean: "admin", "gerente" o "trabajador"
   - Asegurar que todos los campos requeridos estén presentes

3. Errores de importación:
   - Asegurarse de ejecutar uvicorn desde el directorio correcto
   - Verificar que PYTHONPATH incluya el directorio src
