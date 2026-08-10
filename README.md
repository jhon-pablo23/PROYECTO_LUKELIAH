<div align="center">

# 🍰 LUKELIAH

## SISTEMA WEB DE GESTIÓN PARA EMPRENDIMIENTOS DE POSTRES

### Proyecto Full Stack — React + FastAPI + PostgreSQL

</div>

---


## 🎓 Datos académicos

**Institución:** IESTP “Argentina”  
**Proyecto:** LUKELIAH  
**Curso:** Desarrollo de Sistemas de Información  
**Docente:** Ing. Giovanni Ramírez Berrocal

## 👥 Autores

| Integrante | Responsabilidad |
|---|---|
| **Patricia Cuaquira Adco** | Backend |
| **Nombre del integrante** | Frontend |

---


LUKELIAH es un sistema web Full Stack para la gestión de un emprendimiento de postres.

El proyecto integra un backend desarrollado con Python, FastAPI y PostgreSQL y un frontend desarrollado con React, Vite, Bootstrap y Axios, todo dentro de un mismo repositorio.

 Funcionalidades principales

Inicio de sesión de usuarios.
Gestión de usuarios.
Gestión de ingredientes y control de stock.
Gestión de recetas.
Asociación de ingredientes a recetas.
Gestión de postres.
Registro y consulta de ventas.
Detalle de cada venta.
Reportes de ventas por rango de fechas.
Catálogo público de postres.

Las ventas se consideran registros históricos, por lo que pueden registrarse y consultarse, pero no editarse ni eliminarse.

 Tecnologías utilizadas

Backend
Python
FastAPI
Pydantic
PostgreSQL
psycopg2
python-dotenv
Uvicorn
Frontend
React
Vite
Bootstrap
Axios
React Router
Control de versiones
Git
GitHub

 Estructura del proyecto

PROYECTO_LUKELIAH/
│
├── config/                 # Configuración y conexión a PostgreSQL
├── dao/                    # Acceso a datos
├── modelos/                # Modelos del sistema
├── pruebas/                # Archivos de prueba
├── public/                 # Recursos públicos de React
├── routers/                # Endpoints de FastAPI
├── schemas/                # Validación con Pydantic
├── src/                    # Código del frontend React
├── vistas/                 # Vistas del proyecto
│
├── .env                    # Variables locales (NO subir a GitHub)
├── .env.example            # Ejemplo de configuración
├── .gitignore
├── eslint.config.js
├── index.html
├── main.py                 # Punto de entrada del backend
├── package.json
├── package-lock.json
├── requirements.txt
├── script_LUKELIAH.sql
├── vite.config.js
└── README.md

 Arquitectura

React
  ↓
Axios
  ↓
FastAPI - Routers
  ↓
Pydantic - Schemas
  ↓
DAO
  ↓
Modelos
  ↓
PostgreSQL

Routers

Definen los endpoints HTTP de la API REST.

Schemas
Validan los datos de entrada y salida mediante Pydantic.

DAO
Realizan las operaciones de acceso a PostgreSQL.
Modelos
Representan las entidades principales del sistema.
Config
Contiene la configuración general y la conexión a la base de datos.

⚙️ Requisitos previos

Antes de ejecutar el proyecto se necesita:
Git
Python
PostgreSQL
Node.js
npm

 Instalación

1. Clonar el repositorio

git clone URL_DEL_REPOSITORIO
cd PROYECTO_LUKELIAH

Todo el proyecto se ejecuta desde esta misma carpeta raíz.

2. Instalar dependencias del backend

python -m pip install -r requirements.txt

3. Instalar dependencias del frontend

npm install

 Base de datos

4. Crear la base de datos PostgreSQL

Crear una base de datos llamada:

CREATE DATABASE lukeliah_db;

El proyecto también incluye:

script_LUKELIAH.sql

como referencia del modelo de datos.

Las tablas principales son:

usuario
ingrediente
receta
receta_ingrediente
postre
venta
detalle_venta

 Variables de entorno

5. Crear el archivo .env

En la raíz del proyecto crear un archivo .env tomando como referencia .env.example.

Ejemplo:

DB_HOST=localhost
DB_PORT=5432
DB_NAME=lukeliah_db
DB_USER=postgres
DB_PASSWORD=TU_CONTRASENA_POSTGRESQL

VITE_API_URL=http://localhost:8000

Cada integrante debe utilizar sus propias credenciales locales.
.env contiene información local y no debe subirse a GitHub.
.env.example
El repositorio sí debe incluir un archivo .env.example, por ejemplo:

DB_HOST=localhost
DB_PORT=5432
DB_NAME=lukeliah_db
DB_USER=postgres
DB_PASSWORD=TU_CONTRASENA

VITE_API_URL=http://localhost:8000

▶ Ejecutar el sistema

Se deben utilizar dos terminales, ambas ubicadas en la raíz PROYECTO_LUKELIAH.

Terminal 1 — Backend

python -m uvicorn main:app --reload

Backend:

http://localhost:8000

Swagger:

http://localhost:8000/docs

Terminal 2 — Frontend

npm run dev

Frontend:

http://localhost:5173

 Configuración de Axios

La URL del backend debe obtenerse desde la variable de entorno de Vite.

Ejemplo para src/services/api.js:

import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export default api

Esto evita dejar la dirección del backend escrita directamente en el código.

🔗 Endpoints principales

Usuarios

Método

Endpoint

Descripción

GET

/usuarios/

Lista los usuarios

GET

/usuarios/{id_usuario}

Busca un usuario

POST

/usuarios/

Registra un usuario

PUT

/usuarios/{id_usuario}

Actualiza un usuario

DELETE

/usuarios/{id_usuario}

Elimina un usuario

POST

/usuarios/login

Valida las credenciales

Ingredientes

Método

Endpoint

Descripción

GET

/ingredientes/

Lista los ingredientes

GET

/ingredientes/{id_ingrediente}

Busca un ingrediente

POST

/ingredientes/

Registra un ingrediente

PUT

/ingredientes/{id_ingrediente}

Actualiza un ingrediente

DELETE

/ingredientes/{id_ingrediente}

Elimina un ingrediente

Recetas

Método

Endpoint

Descripción

GET

/recetas/

Lista las recetas

GET

/recetas/{id_receta}

Busca una receta

POST

/recetas/

Registra una receta

PUT

/recetas/{id_receta}

Actualiza una receta

DELETE

/recetas/{id_receta}

Elimina una receta

GET

/recetas/{id_receta}/ingredientes

Lista ingredientes de una receta

POST

/recetas/{id_receta}/ingredientes

Agrega un ingrediente

DELETE

/recetas/{id_receta}/ingredientes/{id_ingrediente}

Quita un ingrediente

Postres

Método

Endpoint

Descripción

GET

/postres/

Lista los postres

GET

/postres/{id_postre}

Busca un postre

POST

/postres/

Registra un postre

PUT

/postres/{id_postre}

Actualiza un postre

DELETE

/postres/{id_postre}

Elimina un postre

Ventas

Método

Endpoint

Descripción

GET

/ventas/

Lista las ventas

GET

/ventas/resumen

Resumen de ventas por fechas

GET

/ventas/{id_venta}

Busca una venta

POST

/ventas/

Registra una venta

No existen endpoints PUT ni DELETE para ventas porque se conservan como registros históricos.

Reportes

Ejemplo de consulta:

GET /ventas/resumen?fecha_inicio=2026-08-01&fecha_fin=2026-08-31

Permite obtener:

cantidad de ventas;

total recaudado;

ventas realizadas dentro del rango solicitado.

📚 Swagger / OpenAPI

FastAPI genera documentación automática en:

http://localhost:8000/docs

Desde Swagger es posible:

consultar los endpoints;

revisar los schemas;

probar requests;

observar los códigos de respuesta;

verificar el funcionamiento de la API.

 CORS

Durante el desarrollo, el backend permite la comunicación con el frontend mediante CORSMiddleware.

Orígenes utilizados:

http://localhost:5173
http://localhost:3000

 Archivos que no deben subirse a GitHub

El .gitignore debería incluir como mínimo:

.env
node_modules/
dist/
__pycache__/
*.pyc

No subir:

.env
node_modules/
__pycache__/

Sí subir:

.env.example
requirements.txt
package.json
package-lock.json
script_LUKELIAH.sql
README.md

*Prueba después de clonar

Para comprobar que el repositorio funciona de manera independiente:

1. git clone
2. cd PROYECTO_LUKELIAH
3. python -m pip install -r requirements.txt
4. npm install
5. Crear lukeliah_db en PostgreSQL
6. Crear .env
7. Ejecutar: python -m uvicorn main:app --reload
8. Abrir: http://localhost:8000/docs
9. En otra terminal ejecutar: npm run dev
10. Abrir: http://localhost:5173

El proyecto debe poder ejecutarse sin modificar el código fuente.

Proyecto académico

Proyecto: LUKELIAHTipo: Proyecto Full StackBackend: Python + FastAPI + PostgreSQLFrontend: React + Vite + Bootstrap