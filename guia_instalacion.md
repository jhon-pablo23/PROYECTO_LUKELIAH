#  LUKELIAH — Guía rápida de instalación
Esta guía explica cómo clonar y ejecutar el proyecto **LUKELIAH** en otra computadora.

> Requisito: tener instalado **Python, Git y PostgreSQL**.
---
## 1. Clonar el proyecto
Abrir Git Bash o la terminal de VS Code:
```bash
git clone URL_DEL_REPOSITORIO
```
Entrar a la carpeta:

```bash
cd PROYECTO_LUKELIAH
```
---
## 2. Instalar las dependencias
Todas las dependencias necesarias están en `requirements.txt`.

Ejecutar:
```bash
python -m pip install -r requirements.txt
```
Esto instalará:

- FastAPI
- Uvicorn
- Psycopg2
- Python-dotenv
- Pydantic
--
## 3. Crear la base de datos

Abrir **pgAdmin** y crear la base de datos:
```sql
CREATE DATABASE lukeliah_db;
```

No es necesario crear las tablas manualmente.
Al iniciar el backend, `inicializar()` creará las tablas que todavía no existan.
---
## 4. Crear el archivo `.env`
El archivo `.env` no se encuentra en GitHub porque contiene las credenciales de PostgreSQL.
En la raíz del proyecto crear:
```text
.env
```
Agregar:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=lukeliah_db
DB_USER=postgres
DB_PASSWORD=TU_CONTRASEÑA
```

Reemplazar `TU_CONTRASEÑA` por la contraseña de PostgreSQL de esa computadora.
Ejemplo:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=lukeliah_db
DB_USER=postgres
DB_PASSWORD=123456
```
---
## 5. Ejecutar el backend

Desde la carpeta donde se encuentra `main.py`:

```bash
python -m uvicorn main:app --reload
```
Si todo está correcto aparecerá:

```text
Uvicorn running on http://127.0.0.1:8000
```
---
## 6. Abrir Swagger

Con el servidor funcionando, abrir en el navegador:

```text
http://localhost:8000/docs
```
Desde Swagger se pueden probar los endpoints de:

- Usuarios
- Ingredientes
- Recetas
- Postres
- Ventas
---
#  Resumen rápido

```text
1. git clone URL_DEL_REPOSITORIO

2. cd PROYECTO_LUKELIAH

3. python -m pip install -r requirements.txt

4. Crear en PostgreSQL:
   lukeliah_db

5. Crear .env y colocar:
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=lukeliah_db
   DB_USER=postgres
   DB_PASSWORD=SU_CONTRASEÑA

6. Ejecutar:
   python -m uvicorn main:app --reload

7. Abrir:
   http://localhost:8000/docs
```
---
##  Importante

- No subir el archivo `.env` a GitHub.
- Cada computadora debe tener su propio `.env`.
- La contraseña de PostgreSQL puede ser diferente en cada computadora.
- PostgreSQL debe estar iniciado antes de ejecutar FastAPI.
- Ejecutar los comandos desde la carpeta del proyecto.