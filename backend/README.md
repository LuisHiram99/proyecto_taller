# Backend - Taller Management System

Este es el backend del sistema de gestión para talleres. Proporciona una API REST construida con FastAPI y PostgreSQL.

## Requisitos Previos

- Python 3.8 o superior
- PostgreSQL 12 o superior
- pip (gestor de paquetes de Python)

## Configuración del Entorno

1. Crear un entorno virtual:
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

## Configuración de la Base de Datos

1. Crear la base de datos en PostgreSQL:
```bash
# Conectar a PostgreSQL
psql -U postgres

# Crear la base de datos
CREATE DATABASE taller_db;
```

2. Crear las tablas y tipos necesarios:
```bash
# Desde el directorio raíz del proyecto
cd backend/src/db/schema

# Ejecutar los scripts SQL en orden
psql -U <tu_usuario> -d taller_db -f 001_clientes.sql
psql -U <tu_usuario> -d taller_db -f 002_usuarios.sql
psql -U <tu_usuario> -d taller_db -f 003_carros.sql
psql -U <tu_usuario> -d taller_db -f 004_cliente_carro.sql
psql -U <tu_usuario> -d taller_db -f 005_piezas.sql
psql -U <tu_usuario> -d taller_db -f 006_pieza_carro.sql
psql -U <tu_usuario> -d taller_db -f 007_trabajos.sql
psql -U <tu_usuario> -d taller_db -f 008_trabajo_piezas.sql
psql -U <tu_usuario> -d taller_db -f 009_trabajo_usuarios.sql
```

3. Configurar las variables de entorno:
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

## Ejecutar el Servidor

```bash
# Navegar al directorio src
cd backend/src

# Ejecutar el servidor con recarga automática
PYTHONPATH=$PYTHONPATH:. uvicorn main:app --reload
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