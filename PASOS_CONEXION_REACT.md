# Conectar React (reactxxx) con la API (semana-14)

Guía paso a paso de lo que estamos haciendo para que el frontend en React (`C:\Users\GIOVANNI\Downloads\reactxxx`) consuma esta API en FastAPI (`C:\Users\GIOVANNI\Downloads\semana-14`).

---

## ✅ Paso 1 — Elegir la carpeta correcta de la API

Existían dos copias del proyecto de la API en Descargas:

- `semana-14 -pg4` → tenía varios bugs (ver `ERRORES.md` dentro de esa carpeta).
- `semana-14` → versión correcta, sin esos bugs.

**Decisión:** usar `semana-14` como la API real.

---

## ✅ Paso 2 — Confirmar que la base de datos ya existe

Se revisó PostgreSQL (instalado y corriendo como servicio `postgresql-x64-17`) y ya existía una base de datos llamada **`sistema_db`**, con las 3 tablas ya creadas: `clientes`, `productos`, `ventas`.

No hizo falta crear nada nuevo en PostgreSQL.

---

## ✅ Paso 3 — Crear el archivo `.env`

El código en `config/base_datos.py` necesita las credenciales de la base de datos (host, puerto, nombre, usuario, contraseña), pero no las tiene escritas directamente — las busca en variables de entorno con `os.getenv(...)`.

**Qué se hizo:**

1. Se copió el archivo `.env.example` (ya venía con el proyecto, es una plantilla del profesor) y se renombró a `.env` en la misma carpeta `semana-14`.
2. Se completó con los valores reales:
   ```
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=sistema_db
   DB_USER=postgres
   DB_PASSWORD=admin123
   ```

   (`DB_NAME` se dejó en `sistema_db` porque ese es el nombre real de la base, no `pg4` — ese nombre era solo el de la carpeta del proyecto).

---

## ✅ Paso 4 — Instalar las dependencias de Python

En la carpeta `semana-14`, se ejecutó:

```powershell
pip install -r requirements.txt
```

Esto instaló `fastapi`, `uvicorn`, `psycopg2-binary` y `pydantic`.

---

## ✅ Paso 5 — Primer intento de arrancar el servidor (falló)

```powershell
uvicorn main:app --reload
```

Dio este error:

```
psycopg2.OperationalError: connection to server at "localhost" (::1), port 5432 failed: fe_sendauth: no password supplied
```

**Causa:** en Python, `os.getenv("DB_PASSWORD")` solo lee variables de entorno reales del sistema operativo. Crear el archivo `.env` **no alcanza por sí solo** — hace falta una librería que lo cargue. Sin ella, la contraseña se leía como vacía.

---

## ✅ Paso 6 — Instalar `python-dotenv`

```powershell
pip install python-dotenv
```

Esta librería sabe leer el archivo `.env` y cargar sus valores como si fueran variables de entorno reales.

---

## ✅ Paso 7 — Cargar el `.env` en el código

En `config/base_datos.py`, justo después de los imports existentes, se agregaron estas líneas:

```python
import os
import psycopg2
from psycopg2.extras import RealDictCursor

from dotenv import load_dotenv

load_dotenv()
```

`load_dotenv()` busca el archivo `.env` en la carpeta del proyecto y carga sus variables al entorno del proceso. A partir de ahí, `os.getenv("DB_PASSWORD")` sí encuentra el valor real.

---

## ✅ Paso 8 — Servidor arrancado y verificado

`uvicorn main:app --reload` corrió sin errores y `http://127.0.0.1:8000/docs` cargó bien. La API responde en `http://127.0.0.1:8000/`.

---

## ✅ Paso 9 — Crear un cliente de axios centralizado en React

Se creó el archivo `src/api/axios.js` en el proyecto React (`reactxxx`), con una instancia de axios ya configurada con la URL base del backend:

```js
import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8000",
});

export default api;
```

Así, cualquier componente que necesite llamar a la API hace `import api from "../../api/axios"` y usa `api.get(...)`, `api.post(...)`, etc., sin repetir la URL en cada archivo. Si el backend cambia de puerto o dominio, solo se actualiza en este único lugar.

---

## ✅ Paso 10 — Cargar la lista de clientes desde la API (GET)

En `src/components/clientes/clientes.jsx`, se conectó el componente para que, al abrirse, pida la lista real de clientes a la API en lugar de mostrar los 2 clientes de ejemplo que estaban escritos a mano.

**Qué se hizo:**

1. Se importó `useEffect` (además de `useState`, que ya se usaba) y el cliente de axios creado en el Paso 9:

   ```jsx
   import { useState, useEffect } from "react";
   import api from "../../api/axios";
   ```
2. El estado `clientes` ahora arranca **vacío**, porque los datos van a venir de la API, no de un array fijo:

   ```jsx
   const [clientes, setClientes] = useState([]);
   ```
3. Se agregó un `useEffect` con un array de dependencias vacío (`[]`), lo que hace que se ejecute **una sola vez**, justo cuando el componente termina de montarse en pantalla:

   ```jsx
   useEffect(() => {
     api.get("/clientes/").then((respuesta) => {
       setClientes(respuesta.data);
     });
   }, []);
   ```

   `api.get("/clientes/")` dispara una petición `GET http://localhost:8000/clientes/`. Como es asíncrona, se resuelve con `.then(...)`: cuando la respuesta llega, `respuesta.data` trae el array de clientes en formato JSON (tal como lo devuelve el endpoint `listar_clientes` de `routers/clientes.py`), y `setClientes(...)` lo guarda en el estado para que React vuelva a dibujar la lista con datos reales.

**Requisito:** el servidor de la API (`uvicorn main:app --reload`) debe estar corriendo para que esta petición funcione; si no, la lista queda vacía y no muestra error visible en pantalla (axios lanza una excepción que por ahora no se está capturando — se puede mejorar más adelante con un `.catch(...)`).

---

## ✅ Paso 11 — Que "Crear cliente" guarde en la base de datos real (POST)

Antes, `crearCliente()` solo agregaba el cliente a la lista en memoria del navegador (se perdía al recargar la página). Ahora también lo guarda en PostgreSQL, a través de la API.

**Antes:**

```jsx
function crearCliente() {
  const nuevoCliente = { nombre, ruc, email, telefono };
  setClientes([...clientes, nuevoCliente]);
  setNombre("");
  setRuc("");
  setEmail("");
  setTelefono("");
}
```

**Después:**

```jsx
async function crearCliente() {
  const nuevoCliente = { nombre, ruc, email, telefono };
  const respuesta = await api.post("/clientes/", nuevoCliente);
  setClientes([...clientes, respuesta.data]);
  setNombre("");
  setRuc("");
  setEmail("");
  setTelefono("");
}
```

**Qué cambió y por qué:**

- La función pasó a ser `async` porque ahora tiene que esperar una respuesta de red antes de continuar.
- `await api.post("/clientes/", nuevoCliente)` envía el objeto `nuevoCliente` como el cuerpo (body) de una petición `POST http://localhost:8000/clientes/`. `await` pausa la ejecución de la función hasta que la API responde (no bloquea el navegador, solo esta función).
- Del lado del backend, ese POST llega a `crear_cliente()` en `routers/clientes.py`, que valida los datos con Pydantic (`ClienteCrear`), los guarda en PostgreSQL con `ClienteDAO.insertar()`, y responde con el cliente ya guardado (incluyendo el `id` que le asignó la base de datos).
- Por eso se usa `respuesta.data` (la respuesta real de la API, con `id` incluido) para agregarlo a la lista, en vez de `nuevoCliente` (que no tiene `id` porque ese lo genera PostgreSQL).

**Probado:** se creó un cliente desde el formulario de React y apareció correctamente en la lista, confirmando que el dato quedó guardado en la base de datos real.

---

## ✅ Paso 12 — Eliminar cliente (DELETE)

Se conectó el botón "🗑️ Eliminar" de cada tarjeta para que borre el cliente de verdad en PostgreSQL, no solo de la pantalla.

**Código agregado:**

```jsx
async function eliminarCliente(id) {
  await api.delete(`/clientes/${id}`);
  setClientes(clientes.filter((c) => c.id !== id));
}
```

```jsx
<button className="btn btn-danger btn-sm" onClick={() => eliminarCliente(c.id)}>
  🗑️ Eliminar
</button>
```

**Cómo funciona:**

- `api.delete(`/clientes/${id}`)` — las comillas invertidas (template string) arman la URL insertando el id, por ejemplo `/clientes/3`. Esto dispara `DELETE http://localhost:8000/clientes/3`.
- Del lado del backend, `eliminar_cliente()` en `routers/clientes.py` llama a `ClienteDAO.eliminar()`, que hace el `DELETE FROM clientes WHERE id = %s` en PostgreSQL.
- `await` espera a que la API confirme que se borró antes de seguir.
- `clientes.filter((c) => c.id !== id)` arma una nueva lista sin el cliente borrado, y `setClientes(...)` actualiza la pantalla sin tener que volver a pedir todo a la API de nuevo.

**También se corrigió:** el `key={i}` de cada tarjeta pasó a ser `key={c.id}` — ahora que los clientes vienen de la base de datos, cada uno tiene un `id` real y único, mejor que usar la posición en el array (que puede cambiar al buscar/filtrar).

**Probado:** se eliminó un cliente desde el botón y desapareció de la lista, confirmando que se borró en PostgreSQL.

---

## ✅ Paso 13 — Editar cliente (PUT)

Se conectó el botón "✏️ Editar" para que reutilice el mismo formulario de "Nuevo Cliente": al hacer clic, se cargan los datos del cliente elegido en los inputs, y el mismo botón pasa a **guardar cambios** en vez de crear uno nuevo.

**Parte 1 — guardar qué cliente se está editando y precargar el formulario**

Nuevo estado, junto a los demás `useState`:

```jsx
const [editandoId, setEditandoId] = useState(null);
```

`null` = no se está editando nada. Cuando tiene un número, es el `id` del cliente que se está editando.

Nueva función:

```jsx
function empezarEdicion(c) {
  setNombre(c.nombre);
  setRuc(c.ruc);
  setEmail(c.email);
  setTelefono(c.telefono);
  setEditandoId(c.id);
}
```

Como los inputs del formulario ya estaban conectados con `value={nombre}`, `value={ruc}`, etc., con solo llamar a los `set...` de cada uno se "teletransportan" los datos del cliente elegido al formulario de la izquierda.

Conectado en el botón "✏️ Editar":

```jsx
<button
  className="btn btn-primary btn-sm me-2"
  onClick={() => empezarEdicion(c)}
>
  ✏️ Editar
</button>
```

**Parte 2 — que el botón guarde los cambios (PUT) en vez de crear (POST)**

Se modificó `crearCliente()` para que revise `editandoId` y decida qué hacer:

```jsx
async function crearCliente() {
  if (editandoId) {
    // Modo edición: actualiza el cliente existente
    const respuesta = await api.put(`/clientes/${editandoId}`, {
      nombre,
      email,
      telefono,
    });
    setClientes(
      clientes.map((c) => (c.id === editandoId ? respuesta.data : c)),
    );
    setEditandoId(null);
  } else {
    // Modo creación: como ya estaba
    const nuevoCliente = { nombre, ruc, email, telefono };
    const respuesta = await api.post("/clientes/", nuevoCliente);
    setClientes([...clientes, respuesta.data]);
  }
  setNombre("");
  setRuc("");
  setEmail("");
  setTelefono("");
}
```

**Detalles importantes:**

- El `PUT` **no manda `ruc`** — el schema `ClienteActualizar` del backend (`schemas/cliente_schema.py`) solo acepta `nombre`, `email` y `telefono`; el RUC no se puede cambiar una vez creado el cliente.
- `clientes.map((c) => (c.id === editandoId ? respuesta.data : c))` recorre la lista y **reemplaza únicamente** el cliente editado por la versión actualizada que devolvió la API; los demás quedan igual.
- `setEditandoId(null)` al final "apaga" el modo edición, para que el botón vuelva a comportarse como "crear".

Y el botón cambia de texto según el modo:

```jsx
<button className="btn btn-success mt-3" onClick={crearCliente}>
  {editandoId ? "Guardar cambios" : "+ Crear cliente"}
</button>
```

**Probado:** se editó el apellido de un cliente desde el formulario, se guardó con "Guardar cambios", y el cambio se reflejó correctamente en la tarjeta y en PostgreSQL.

---

## 🎉 `clientes.jsx` — CRUD completo conectado a la API

GET (listar), POST (crear), PUT (editar), DELETE (eliminar) — los 4 ya funcionan contra la base de datos real.

---

## ✅ Paso 14 — Cargar la lista de productos desde la API (GET)

Mismo patrón que se usó en `clientes.jsx` (Paso 10), aplicado a `src/components/productos/productos.jsx`.

1. Import de `useEffect` y del cliente de axios:

   ```jsx
   import { useState, useEffect } from "react";
   import api from "../../api/axios";
   ```
2. `productos` arranca vacío en vez de con los 3 productos de ejemplo escritos a mano:

   ```jsx
   const [productos, setProductos] = useState([]);
   ```
3. `useEffect` que pide la lista real al montar el componente:

   ```jsx
   useEffect(() => {
     api.get("/productos/").then((respuesta) => {
       setProductos(respuesta.data);
     });
   }, []);
   ```

**Probado:** al abrir la sección Productos aparecen los 5 productos reales que hay en PostgreSQL (Laptop Lenovo, Mouse Logitech, Teclado Mecánico, Monitor 24", Kerosne), no los 3 de ejemplo que estaban antes.

---

## ✅ Paso 15 — Que "Crear producto" guarde en la base de datos (POST)

```jsx
async function crearProducto() {
  const nuevoProducto = { nombre, precio };
  const respuesta = await api.post("/productos/", nuevoProducto);
  setProductos([...productos, respuesta.data]);
  setNombre("");
  setPrecio("");
  setMostrarFormulario(false);
}
```

**Cómo funciona:**

- `api.post("/productos/", nuevoProducto)` envía `POST http://localhost:8000/productos/` con el nombre y precio escritos en el formulario.
- El backend (`crear_producto()` en `routers/productos.py`) valida los datos con el schema `ProductoCrear` y los guarda con `ProductoDAO.insertar()`, devolviendo el producto ya guardado (con su `id` real).
- `respuesta.data` (no `nuevoProducto`) se usa para agregarlo a la lista, porque trae el `id` asignado por PostgreSQL.

**Nota sobre el precio:** el input es `type="number"`, pero React igual guarda su valor como texto en el estado (`precio` es un string, ej. `"85.00"`). No hizo falta convertirlo con `Number(precio)` antes de enviarlo — se probó directamente contra la API y Pydantic (la librería de validación del backend) acepta y convierte automáticamente strings numéricos a `float`.

**Probado:** se creó un producto nuevo ("Inka Cola") desde el formulario y apareció correctamente en la tabla, confirmando que quedó guardado en PostgreSQL.

---

## ✅ Paso 16 — Eliminar producto (DELETE)

Mismo patrón que el Paso 12 (eliminar cliente), aplicado a productos.

```jsx
async function eliminarProducto(id) {
  await api.delete(`/productos/${id}`);
  setProductos(productos.filter((p) => p.id !== id));
}
```

```jsx
<button
  className="btn btn-outline-danger btn-sm"
  onClick={() => eliminarProducto(p.id)}
>
  Eliminar
</button>
```

- `api.delete(`/productos/${id}`)` dispara `DELETE http://localhost:8000/productos/{id}`, que en el backend (`eliminar_producto()` en `routers/productos.py`) borra el registro en PostgreSQL.
- `productos.filter((p) => p.id !== id)` quita ese producto de la lista en pantalla sin volver a pedir todo de nuevo a la API.

**Probado:** se eliminó un producto desde el botón de la tabla y desapareció correctamente, confirmando que se borró en PostgreSQL.

---

## ✅ Paso 17 — Agregar el endpoint `PUT /productos/{id}` en la API

Faltaba conectar una ruta para actualizar productos. El DAO (`ProductoDAO.actualizar()`) y el schema (`ProductoActualizar`) ya existían en el proyecto, pero no había ningún endpoint que los usara.

En `routers/productos.py`, entre el `POST` y el `DELETE`, se agregó:

```python
# PUT /productos/{prod_id} — actualiza un producto existente
@router.put("/{prod_id}", response_model=ProductoRespuesta)
def actualizar_producto(prod_id: int, datos: ProductoActualizar):
    try:
        p = dao.actualizar(prod_id, datos.nombre, datos.precio)
        return p.to_dict()
    except ProductoNoEncontradoError as ex:
        raise HTTPException(status_code=404, detail=str(ex))
```

Sigue exactamente el mismo patrón que `actualizar_cliente()` en `routers/clientes.py`: recibe el `id` por la URL y los campos a cambiar en el body (validados por `ProductoActualizar`), delega en el DAO, y devuelve 404 si el producto no existe.

**Verificado:** `uvicorn --reload` recargó solo, y `PUT /productos/{prod_id}` ya aparece en `http://127.0.0.1:8000/docs` junto a `GET` y `DELETE`.

---

## ✅ Paso 18 — Cargar los datos del producto en el formulario (parte 1 de editar en React)

Mismo patrón que `empezarEdicion` en `clientes.jsx` (Paso 13), adaptado a productos.

Nuevo estado, junto a `mostrarFormulario`:

```jsx
const [editandoId, setEditandoId] = useState(null);
```

Nueva función:

```jsx
function empezarEdicion(p) {
  setNombre(p.nombre);
  setPrecio(p.precio);
  setEditandoId(p.id);
  setMostrarFormulario(true);
}
```

A diferencia de clientes (donde el formulario siempre está visible), en productos el formulario empieza escondido — por eso acá se agrega `setMostrarFormulario(true)`, para que se abra automáticamente al hacer clic en "Editar".

Conectado en el botón:

```jsx
<button className="btn btn-outline-primary btn-sm me-2" onClick={() => empezarEdicion(p)}>
  Editar
</button>
```

**Probado:** al hacer clic en "Editar" en una fila, el formulario se abre solo y aparece con el nombre y precio de ese producto ya cargados.

---

## ✅ Paso 19 — Que "Editar" guarde los cambios (parte 2: PUT en React)

Igual que en el Paso 13 de `clientes.jsx`, se modificó `crearProducto()` para que revise `editandoId` y decida entre actualizar o crear:

```jsx
async function crearProducto() {
  if (editandoId) {
    // Modo edición: actualiza el producto existente
    const respuesta = await api.put(`/productos/${editandoId}`, {
      nombre,
      precio: Number(precio),
    });
    setProductos(
      productos.map((p) => (p.id === editandoId ? respuesta.data : p)),
    );
    setEditandoId(null);
  } else {
    // Modo creación: como ya estaba
    const nuevoProducto = { nombre, precio: Number(precio) };
    const respuesta = await api.post("/productos/", nuevoProducto);
    setProductos([...productos, respuesta.data]);
  }
  setNombre("");
  setPrecio("");
  setMostrarFormulario(false);
}
```

Y el botón cambia de texto según el modo:

```jsx
<button className="btn btn-primary mt-3 me-2" onClick={crearProducto}>
  {editandoId ? "Guardar cambios" : "Crear producto"}
</button>
```

**Cómo funciona:** `api.put(`/productos/${editandoId}`, {...})` llama al endpoint agregado en el Paso 17. `productos.map((p) => (p.id === editandoId ? respuesta.data : p))` reemplaza únicamente el producto editado por la versión actualizada que devolvió la API, dejando los demás igual. `setEditandoId(null)` al final apaga el modo edición.

**Probado:** se editó el precio de un producto, se guardó con "Guardar cambios", y el cambio se reflejó en la tabla y en PostgreSQL.

---

## 🎉 `productos.jsx` — CRUD completo conectado a la API

GET, POST, PUT y DELETE ya funcionan contra la base de datos real.

---

## ✅ Paso 20 — Cargar clientes y productos reales en los desplegables de Ventas

`ventas.jsx` es más complejo que los otros dos componentes: además de la lista de ventas, tiene dos `<select>` (cliente y producto) que antes mostraban listas escritas a mano. Se conectaron a la API real.

**Antes:**

```jsx
const clientesDisponibles = [
  { id: 1, nombre: "Jose Perez Guerra" },
  { id: 2, nombre: "Jossi Lavado" },
];
const productosDisponibles = [
  { id: 1, nombre: "Laptop Asus", precio: 5896.0 },
  { id: 2, nombre: "Teclado Micronic", precio: 145.89 },
  { id: 3, nombre: "Monitor lg", precio: 249.99 },
];
```

**Después:**

```jsx
const [clientesDisponibles, setClientesDisponibles] = useState([]);
const [productosDisponibles, setProductosDisponibles] = useState([]);

useEffect(() => {
  api.get("/clientes/").then((respuesta) => {
    setClientesDisponibles(respuesta.data);
  });
  api.get("/productos/").then((respuesta) => {
    setProductosDisponibles(respuesta.data);
  });
}, []);
```

**Detalle importante (error corregido en el camino):** al principio se dejaron `clientesDisponibles` y `productosDisponibles` como constantes normales (`const clientesDisponibles = []`) en vez de `useState`. Como el `useEffect` llamaba a `setClientesDisponibles(...)` y `setProductosDisponibles(...)`, y esas funciones solo existen cuando la variable se declara con `useState`, la página fallaba con `setClientesDisponibles is not defined`. Se corrigió declarando ambas listas con `useState([])`.

**Por qué dos peticiones dentro del mismo `useEffect`:** ambas son independientes entre sí (una trae clientes, otra productos), así que se lanzan las dos sin esperar a que termine la primera — cada una actualiza su propio estado cuando responde.

**Probado:** al abrir la sección Ventas, los desplegables "Seleccionar cliente" y "Seleccionar producto" muestran los datos reales de PostgreSQL.

---

## ✅ Paso 21 — Cargar el historial de ventas desde la API (GET)

Se reemplazaron las 2 ventas de ejemplo escritas a mano por las reales, pedidas a la API.

```jsx
const [ventas, setVentas] = useState([]);
```

Y dentro del mismo `useEffect` que ya cargaba clientes y productos (Paso 20), se agregó una tercera petición:

```jsx
useEffect(() => {
  api.get("/clientes/").then((respuesta) => {
    setClientesDisponibles(respuesta.data);
  });
  api.get("/productos/").then((respuesta) => {
    setProductosDisponibles(respuesta.data);
  });
  api.get("/ventas/").then((respuesta) => {
    setVentas(respuesta.data);
  });
}, []);
```

`GET /ventas/` en el backend (`listar_ventas()` en `routers/ventas.py`) devuelve las ventas ya con los nombres de cliente y producto incluidos (gracias al JOIN que hace `VentaDAO.obtener_todos()`), no solo los ids — por eso la tabla de React puede mostrar `v.cliente` y `v.producto` directamente sin tener que cruzarlos a mano.

**Verificado con pgAdmin:** se revisó la tabla `ventas` directamente en PostgreSQL (Servers → sistema_db → Schemas → public → Tables → ventas → View/Edit Data) y los 4 registros ahí coinciden con los que muestra la tabla en React.

---

## ✅ Paso 22 — Que "Registrar venta" guarde en la base de datos (POST)

```jsx
async function crearVenta() {
  const nuevaVenta = {
    cliente_id: Number(clienteId),
    producto_id: Number(productoId),
    cantidad: Number(cantidad),
  };
  const respuesta = await api.post("/ventas/", nuevaVenta);
  setVentas([...ventas, respuesta.data]);
  setClienteId("");
  setProductoId("");
  setCantidad("");
  setFecha("");
  setMostrarFormulario(false);
}
```

**Por qué quedó más simple que antes:** ya no hace falta buscar el cliente/producto en un array local ni calcular el total a mano — eso ahora lo hace el backend. `registrar_venta()` en `routers/ventas.py` recibe solo `cliente_id`, `producto_id` y `cantidad`, y `VentaDAO.registrar()` calcula el `total` (precio del producto × cantidad) y la `fecha` (hora del servidor en el momento de guardar) automáticamente. La API devuelve la venta ya completa —con nombres de cliente/producto, fecha y total incluidos— y esa respuesta (`respuesta.data`) es lo que se agrega a la lista.

**Nota:** el input de fecha (`type="datetime-local"`) del formulario quedó sin efecto — la API ignora cualquier fecha que se le mande y siempre usa la hora del servidor. Queda pendiente decidir si se quita ese input del formulario más adelante.

**Probado:** se registró una venta desde el formulario de React y apareció en PostgreSQL con el total calculado correctamente y la fecha real del servidor.

---

## ✅ Paso 23 — Decisión: las ventas no se eliminan ni se editan

Se discutió qué hacer con el botón "Eliminar" de ventas, ya que la API nunca tuvo `DELETE /ventas/{id}` (ni `PUT`).

**Por qué:** en un sistema real de ventas/facturación, los comprobantes no se borran ni se modifican una vez emitidos — por temas de auditoría y contabilidad, se "anulan" (quedan guardados pero marcados como cancelados). El backend de este proyecto ya refleja esa idea: `schemas/venta_schema.py` tiene el comentario *"Las ventas no tienen schema de actualizar porque son inmutables"*, y nunca se implementó `PUT` ni `DELETE` para ventas.

**Opciones consideradas:**

1. Agregar `DELETE /ventas/{id}` en la API (rápido, pero no realista).
2. Implementar "anular/activar" con un campo de estado (más realista, pero bastante más trabajo: columna nueva en la tabla, cambios en el DAO, en el listado, etc.).
3. Quitar el botón "Eliminar" de la interfaz, dejando las ventas como registro fijo — igual que ya están diseñadas en el backend.

**Decisión:** opción 3, por ahora. No se agrega funcionalidad nueva al backend; se ajusta el frontend para que no ofrezca una acción que el sistema no soporta.

**Cambios en `ventas.jsx`:**

- Se eliminó la función `eliminarVenta(id)`.
- Se quitó la columna `<th>Acciones</th>` del encabezado de la tabla.
- Se quitó la celda `<td>` con el botón "Eliminar" de cada fila.

El input de fecha del formulario (que tampoco tiene efecto, ver Paso 22) se dejó como está por ahora.

---

## 🎉 `ventas.jsx` — conectado a la API (GET, POST; sin editar/eliminar por diseño)

---

## Historial — decisión: construirlo con base de datos, no en memoria

`historial.jsx` (la 4ta sección del menú) mostraba datos de ejemplo fijos, sin conexión real. Al revisar la API se encontró que existe una clase `Logger` (`config/logger.py`, patrón Singleton) que ya registra internamente cada acción de `ClienteDAO`, `ProductoDAO` y `VentaDAO` (crear, actualizar, eliminar), pero:

- Vive solo en memoria RAM de Python, no en PostgreSQL.
- No estaba expuesta por ningún endpoint HTTP.

Se evaluaron dos caminos:

1. **Versión simple**: exponer el `Logger` en memoria con un endpoint nuevo (`GET/DELETE /historial/`). Rápido, pero se pierde todo cada vez que el servidor se reinicia (pasa seguido con `uvicorn --reload`, cada vez que se guarda un archivo `.py`).
2. **Versión con base de datos**: crear una tabla `historial` en PostgreSQL, para que el registro sea permanente.

Se armó primero la versión simple (endpoint `GET/DELETE /historial/` leyendo `Logger().obtener_logs()`) y se comprobó en vivo el problema: al guardar archivos del backend durante el desarrollo, el servidor se reiniciaba y el historial se vaciaba solo. **Decisión final: construirlo con base de datos**, para que sea permanente. La versión simple no se documenta como paso oficial porque quedó reemplazada.

---

## ✅ Paso 24 — Crear la tabla `historial` en PostgreSQL

Se agregó a `config/base_datos.py`, en la función `inicializar()`, siguiendo el mismo patrón que las otras 3 tablas (`CREATE TABLE IF NOT EXISTS`, se crea sola al arrancar el servidor):

```python
# Tabla de historial: registra cada acción importante del sistema
# (crear/editar/eliminar cliente, producto o venta) de forma permanente.
cursor.execute("""
    CREATE TABLE IF NOT EXISTS historial (
        id     SERIAL PRIMARY KEY,
        fecha  TEXT   NOT NULL,
        hora   TEXT   NOT NULL,
        accion TEXT   NOT NULL
    )
""")
```

**Aclaración sobre `script_bd.sql` vs `base_datos.py`:** el proyecto tiene dos formas independientes de crear tablas. `script_bd.sql` se corre manualmente en pgAdmin (además inserta datos de ejemplo). `base_datos.py` → `inicializar()` corre automáticamente cada vez que arranca el servidor, y sirve de respaldo aunque nunca hayas corrido el script SQL. Por eso alcanza con agregar `historial` solo acá; no fue necesario tocar `script_bd.sql`.

**Verificado:** con `\d historial` en psql se confirmó que la tabla se creó con las columnas `id`, `fecha`, `hora`, `accion`.

---

## ✅ Paso 25 — Crear el modelo `Historial`

Se creó `modelos/historial.py`, siguiendo el mismo patrón que `modelos/cliente.py` y `modelos/producto.py`:

```python
class Historial:
    def __init__(self, fecha, hora, accion):
        self.id = None
        self.fecha = fecha
        self.hora = hora
        self.accion = accion

    def to_dict(self):
        return {
            "id": self.id,
            "fecha": self.fecha,
            "hora": self.hora,
            "accion": self.accion,
        }
```

`id` empieza en `None` porque lo asigna PostgreSQL (`SERIAL`) al insertar. `to_dict()` sirve para que la API pueda convertir el objeto a JSON.

---

## ✅ Paso 26 — Crear el DAO `HistorialDAO`

Se creó `dao/historial_dao.py`:

```python
from config.base_datos import obtener_conexion
from modelos.historial import Historial

class HistorialDAO:
    def insertar(self, h):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO historial (fecha, hora, accion) VALUES (%s, %s, %s) RETURNING id",
            (h.fecha, h.hora, h.accion)
        )
        h.id = cursor.fetchone()["id"]
        conn.commit()
        conn.close()
        return h

    def obtener_todos(self):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM historial ORDER BY id DESC")
        filas = cursor.fetchall()
        conn.close()
        return [self.__fila_a_historial(f) for f in filas]

    def limpiar(self):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM historial")
        conn.commit()
        conn.close()

    def __fila_a_historial(self, fila):
        h = Historial(fila["fecha"], fila["hora"], fila["accion"])
        h.id = fila["id"]
        return h
```

**Detalles:**

- `insertar()` sigue el mismo patrón que `ClienteDAO`/`ProductoDAO`: `RETURNING id` para obtener el id que le asignó PostgreSQL.
- `obtener_todos()` ordena con `ORDER BY id DESC` — al revés que las otras tablas — para que las acciones **más recientes aparezcan primero** en el historial (tiene más sentido leerlo así).
- `limpiar()` es nuevo, no existe en los otros DAOs: hace `DELETE FROM historial` sin condición, borra todas las filas. Lo va a usar el botón "Limpiar historial".
- No tiene excepciones personalizadas (`NoEncontradoError`, etc.) porque el historial no se busca por id ni se actualiza, solo se agrega, se lista y se limpia por completo.

---

## ✅ Paso 27 — Crear el schema `HistorialRespuesta`

Se creó `schemas/historial_schema.py`:

```python
from pydantic import BaseModel

class HistorialRespuesta(BaseModel):
    id: int
    fecha: str
    hora: str
    accion: str
```

A diferencia de `ClienteCrear`/`ProductoCrear`/`VentaCrear`, **no hay un schema de "Crear"** para historial — no existe un `POST /historial/` que reciba datos desde afuera. Cada fila se genera automáticamente del lado del servidor cuando `ClienteDAO`, `ProductoDAO` o `VentaDAO` registran una acción (eso se conecta en el siguiente paso).

---

## ✅ Paso 28 — Actualizar `routers/historial.py` para usar la tabla real

Se reemplazó el contenido del router (que antes usaba `Logger().obtener_logs()` / `Logger().limpiar()`, la versión en memoria) para que use `HistorialDAO` en su lugar:

```python
from fastapi import APIRouter
from dao.historial_dao import HistorialDAO
from schemas.historial_schema import HistorialRespuesta

router = APIRouter(prefix="/historial", tags=["Historial"])
dao = HistorialDAO()

@router.get("/", response_model=list[HistorialRespuesta])
def listar_historial():
    return [h.to_dict() for h in dao.obtener_todos()]

@router.delete("/")
def limpiar_historial():
    dao.limpiar()
    return {"mensaje": "Historial limpiado"}
```

Mismo patrón que `routers/productos.py`: `dao = HistorialDAO()` a nivel de módulo (compartido entre todas las peticiones), `response_model=list[HistorialRespuesta]` para que FastAPI valide y documente la respuesta, y `to_dict()` para convertir cada objeto `Historial` en un diccionario serializable a JSON.

---

## ✅ Paso 29 — Método `registrar()` en `HistorialDAO`

Para no repetir la lógica de fecha/hora en cada DAO que necesite escribir al historial, se agregó un método centralizado:

```python
from datetime import datetime
...

def registrar(self, accion):
    ahora = datetime.now()
    h = Historial(
        fecha=ahora.strftime("%d/%m/%Y"),
        hora=ahora.strftime("%H:%M:%S"),
        accion=accion,
    )
    self.insertar(h)
```

Así, `ClienteDAO`, `ProductoDAO` y `VentaDAO` solo van a necesitar llamar a `HistorialDAO().registrar("texto de la acción")` en el siguiente paso, sin preocuparse por armar la fecha/hora ellos mismos.

---

## ✅ Paso 30 — Conectar `ClienteDAO` con el historial

En `dao/cliente_dao.py`:

- Se importó `HistorialDAO` y se agregó `self.__hdao = HistorialDAO()` en `ClienteDAO.__init__`.
- En `insertar()`, `actualizar()` y `eliminar()`, justo después de cada `self.__log.info(...)` que confirma el éxito de la operación, se agregó la línea equivalente con `self.__hdao.registrar(...)`, con el mismo texto:
  ```python
  self.__log.info(f"Cliente agregado: {cliente.nombre} (ID={cliente.id})")
  self.__hdao.registrar(f"Cliente agregado: {cliente.nombre} (ID={cliente.id})")
  ```

  (y lo mismo para "Cliente actualizado" y "Cliente eliminado").

**Probado:** se creó y se eliminó un cliente de prueba directamente contra la API, y ambas acciones aparecieron correctamente en `GET /historial/`, con fecha, hora y descripción — confirmando que `ClienteDAO` quedó bien conectado con `historial`.

---

## ✅ Paso 31 — Conectar `ProductoDAO` con el historial

Mismo patrón que `ClienteDAO` (Paso 30). En `dao/producto_dao.py`:

- Se importó `HistorialDAO` y se agregó `self.__hdao = HistorialDAO()` en `ProductoDAO.__init__`.
- En `insertar()`, `actualizar()` y `eliminar()`, justo después de cada `self.__log.info(...)`, se agregó la línea equivalente con `self.__hdao.registrar(...)`, con el mismo texto:
  ```python
  self.__log.info(f"Producto agregado: {p.nombre} S/.{p.precio:.2f} (ID={p.id})")
  self.__hdao.registrar(f"Producto agregado: {p.nombre} S/.{p.precio:.2f} (ID={p.id})")
  ```

  (y lo mismo para "Producto actualizado" y "Producto eliminado").

**Probado:** se creó y se eliminó un producto de prueba directamente contra la API, y la acción "Producto agregado" apareció correctamente en `GET /historial/`.

---

## ✅ Paso 32 — Conectar `VentaDAO` con el historial

Mismo patrón que `ClienteDAO` y `ProductoDAO`. En `dao/venta_dao.py`:

- Se importó `HistorialDAO` y se agregó `self.__hdao = HistorialDAO()` en `VentaDAO.__init__`.
- En `registrar()` (el único método que crea una venta), justo después de `self.__log.info(...)`, se agregó:
  ```python
  self.__log.info(f"Venta registrada: ID={venta.id} Total=S/.{venta.total:.2f}")
  self.__hdao.registrar(f"Venta registrada: ID={venta.id} Total=S/.{venta.total:.2f}")
  ```

**Probado:** se registró una venta de prueba directamente contra la API y apareció correctamente en `GET /historial/`.

Con esto, los 3 DAOs (`ClienteDAO`, `ProductoDAO`, `VentaDAO`) quedan conectados al historial — toda acción de creación se registra automáticamente.

---

## ✅ Paso 33 — Conectar `historial.jsx` con la API real

Ya existía la conexión `GET /historial/` de la versión simple anterior, pero hicieron falta 2 ajustes por el cambio de formato de los datos:

1. La API nueva devuelve el campo `accion` (no `msg`, que era del `Logger` viejo). Se cambió:

   ```jsx
   <td>{h.msg}</td>
   ```

   por:

   ```jsx
   <td>{h.accion}</td>
   ```
2. El botón "Limpiar historial" solo vaciaba la lista en pantalla, sin avisarle a la API. Se cambió:

   ```jsx
   function limpiarHistorial() {
     setHistorial([]);
   }
   ```

   por:

   ```jsx
   async function limpiarHistorial() {
     await api.delete("/historial/");
     setHistorial([]);
   }
   ```

**Probado:** se crearon acciones reales (producto actualizado, venta registrada) desde React, y aparecieron correctamente en la tabla de Historial con fecha, hora y descripción.

---

## ✅ Paso 34 — Mejorar el mensaje de "Venta registrada" en el historial

Al probarlo, se notó que el mensaje de las ventas era menos informativo que el de clientes/productos: decía `"Venta registrada: ID=7 Total=S/.39.45"` (solo el id de la venta), en vez de mostrar quién compró qué.

**Causa:** `VentaDAO.registrar()` solo tenía a mano el id de la venta y el total — el nombre del cliente y del producto no se le pasaban.

**Cambios:**

- `dao/venta_dao.py` — el método pasó de `registrar(self, venta, precio_producto)` a `registrar(self, venta, precio_producto, nombre_cliente, nombre_producto)`, y el mensaje del historial cambió a:
  ```python
  f"Venta registrada: {nombre_cliente} compró {venta.cantidad}x {nombre_producto} (Total: S/.{venta.total:.2f})"
  ```
- `routers/ventas.py` — se actualizó la llamada para pasarle los nombres, que esa función ya tenía a mano (`c` y `p`, el cliente y producto ya buscados antes):
  ```python
  v = vdao.registrar(Venta(datos.cliente_id, datos.producto_id, datos.cantidad), p.precio, c.nombre, p.nombre)
  ```

**Probado:** una venta nueva generó el mensaje `"Venta registrada: Luis Torres compró 1x Laptop Lenovo (Total: S/.3600.00)"` en el historial.

---

## 🎉 Historial conectado con base de datos real (permanente)

`clientes.jsx`, `productos.jsx`, `ventas.jsx` e `historial.jsx` — las 4 secciones del sistema — quedan conectadas a la API real con datos persistentes en PostgreSQL.

---

## ✅ Paso 35 — Mejorar los mensajes de "Cliente actualizado" y "Producto actualizado"

Mismo problema que se corrigió para ventas (Paso 34): al editar un cliente o producto, el historial solo mostraba el `ID`, sin el nombre — a diferencia de "agregado" y "eliminado", que sí lo incluían.

**`dao/producto_dao.py`**, dentro de `actualizar()`:

```python
# Antes
self.__hdao.registrar(f"Producto actualizado: ID={prod_id}")
# Después
self.__hdao.registrar(f"Producto actualizado: {nuevo_nombre} (ID={prod_id})")
```

**`dao/cliente_dao.py`**, dentro de `actualizar()`:

```python
# Antes
self.__hdao.registrar(f"Cliente actualizado: ID={cliente_id}")
# Después
self.__hdao.registrar(f"Cliente actualizado: {nuevo_nombre} (ID={cliente_id})")
```

En ambos casos, `nuevo_nombre` ya estaba calculado un poco más arriba en la misma función (es el nombre nuevo si se envió uno, o el que ya tenía si no se cambió), así que no hizo falta buscar nada extra.

**Probado:** se actualizó un producto y un cliente reales por la API, y el historial mostró `"Producto actualizado: Inka Cola Plus +++ (ID=7)"` y `"Cliente actualizado: Luis Torres (ID=2)"` correctamente.

---

## 🔜 Próximos pasos (aún no hechos)

- [ ] Verificar que React (`reactxxx`, corre en `http://localhost:5173`) puede llamar a la API sin errores de CORS (ya está configurado en `main.py` para aceptar ese puerto).
- [ ] Probar el flujo completo de las 3 secciones (clientes, productos, ventas) juntas desde React.
