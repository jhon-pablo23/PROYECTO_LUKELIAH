from config.base_datos import obtener_conexion
from modelos.usuario import Usuario


class CorreoDuplicadoError(Exception):
    def __init__(self, correo):
        super().__init__(f"El correo '{correo}' ya está registrado")


class UsuarioDAO:
    def obtener_todos(self):
        # Se excluye la contraseña de la consulta por seguridad.
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT id_usuario, nombre, correo FROM usuario ORDER BY id_usuario")
        filas = cursor.fetchall()
        conn.close()
        return filas

    def buscar_por_id(self, id_usuario):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT id_usuario, nombre, correo FROM usuario WHERE id_usuario = %s", (id_usuario,))
        fila = cursor.fetchone()
        conn.close()
        return fila

    def buscar_por_correo(self, correo):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuario WHERE correo = %s", (correo,))
        fila = cursor.fetchone()
        conn.close()
        return fila

    def insertar(self, usuario):
    # Verifica previamente que el correo no esté registrado.
        if self.buscar_por_correo(usuario.correo):
            raise CorreoDuplicadoError(usuario.correo)
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO usuario (nombre, correo, contrasena) VALUES (%s, %s, %s) RETURNING id_usuario",
            (usuario.nombre, usuario.correo, usuario.contrasena),
        )
        usuario.id_usuario = cursor.fetchone()["id_usuario"]
        conn.commit()
        conn.close()
        return usuario

    def actualizar(self, id_usuario, nombre=None, correo=None, contrasena=None):
        actual = self.buscar_por_id(id_usuario)
        if not actual:
            return None
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE usuario SET nombre = %s, correo = %s, "
            "contrasena = COALESCE(%s, contrasena) WHERE id_usuario = %s "
            "RETURNING id_usuario, nombre, correo",
            (nombre or actual["nombre"], correo or actual["correo"], contrasena, id_usuario),
        )
        fila = cursor.fetchone()
        conn.commit()
        conn.close()
        return fila

    def eliminar(self, id_usuario):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM usuario WHERE id_usuario = %s", (id_usuario,))
        conn.commit()
        conn.close()

    def verificar_credenciales(self, correo, contrasena):
        usuario = self.buscar_por_correo(correo)
        if usuario and usuario["contrasena"] == contrasena:
            return {"id_usuario": usuario["id_usuario"], "nombre": usuario["nombre"], "correo": usuario["correo"]}
        return None
