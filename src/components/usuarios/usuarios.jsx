import { useEffect, useState } from "react";
import api from "../../api/axios";
import "./usuarios.css";

function Usuarios() {

    const [nombre, setNombre] = useState("");
    const [correo, setCorreo] = useState("");
    const [contrasena, setContrasena] = useState("");
    const [buscar, setBuscar] = useState("");
    const [mostrarFormulario, setMostrarFormulario] = useState(false);

    const [usuarios, setUsuarios] = useState([]);

    useEffect(() => {
        cargarUsuarios();
    }, []);

    async function cargarUsuarios() {
        try {
            const respuesta = await api.get("/usuarios/");
            setUsuarios(respuesta.data);
        } catch (error) {
            console.error("Error al cargar usuarios:", error);
        }
    }

    async function agregarUsuario(evento) {
        evento.preventDefault();

        if (nombre === "" || correo === "" || contrasena === "") {
            alert("Todos los campos son obligatorios");
            return;
        }

        const nuevoUsuario = {
            nombre: nombre,
            correo: correo,
            contrasena: contrasena
        };

        try {
            const respuesta = await api.post(
                "/usuarios/",
                nuevoUsuario
            );

            setUsuarios([...usuarios, respuesta.data]);

            setNombre("");
            setCorreo("");
            setContrasena("");

            setMostrarFormulario(false);

        } catch (error) {
            console.error("Error al crear usuario:", error);

            if (error.response && error.response.data) {
                alert(
                    error.response.data.detail ||
                    "No se pudo crear el usuario."
                );
            } else {
                alert("No se pudo crear el usuario.");
            }
        }
    }

    function eliminarUsuario(id) {
        const listaNueva = usuarios.filter(
            (usuario) => usuario.id !== id
        );

        setUsuarios(listaNueva);
    }

    const usuariosFiltrados = usuarios.filter((usuario) =>
        usuario.nombre.toLowerCase().includes(buscar.toLowerCase()) ||
        usuario.correo.toLowerCase().includes(buscar.toLowerCase())
    );

    return (
        <div className="usuarios">

            {/* ENCABEZADO */}

            <div className="usuarios-header">

                <div>
                    <h1>Usuarios</h1>
                    <p>Gestiona los administradores de LUKELIAH</p>
                </div>

                <button
                    type="button"
                    className="btn-nuevo-usuario"
                    onClick={() =>
                        setMostrarFormulario(!mostrarFormulario)
                    }
                >
                    Nuevo Usuario
                </button>

            </div>


            {/* BUSCADOR */}

            <div className="usuarios-toolbar">

                <input
                    type="text"
                    className="buscar-usuario"
                    placeholder="Buscar usuarios..."
                    value={buscar}
                    onChange={(evento) =>
                        setBuscar(evento.target.value)
                    }
                />

            </div>


            {/* FORMULARIO */}

            {mostrarFormulario && (

                <div className="usuario-form-card">

                    <h2>Nuevo usuario</h2>

                    <form onSubmit={agregarUsuario}>

                        <div className="form-row">

                            <div className="form-group">

                                <label>Nombre</label>

                                <input
                                    type="text"
                                    className="form-control"
                                    value={nombre}
                                    onChange={(evento) =>
                                        setNombre(evento.target.value)
                                    }
                                    placeholder="Ingrese el nombre"
                                />

                            </div>


                            <div className="form-group">

                                <label>Correo</label>

                                <input
                                    type="email"
                                    className="form-control"
                                    value={correo}
                                    onChange={(evento) =>
                                        setCorreo(evento.target.value)
                                    }
                                    placeholder="correo@ejemplo.com"
                                />

                            </div>


                            <div className="form-group">

                                <label>Contrasena</label>

                                <input
                                    type="password"
                                    className="form-control"
                                    value={contrasena}
                                    onChange={(evento) =>
                                        setContrasena(evento.target.value)
                                    }
                                    placeholder="Ingrese la contrasena"
                                />

                            </div>

                        </div>


                        <div className="form-buttons">

                            <button
                                type="submit"
                                className="btn btn-primary"
                            >
                                Crear usuario
                            </button>

                            <button
                                type="button"
                                className="btn btn-secondary"
                                onClick={() =>
                                    setMostrarFormulario(false)
                                }
                            >
                                Cancelar
                            </button>

                        </div>

                    </form>

                </div>

            )}


            {/* LISTA DE USUARIOS */}

            <div className="usuarios-table-card">

                <h2>Lista de usuarios</h2>

                <div className="table-responsive">

                    <table className="table table-hover">

                        <thead>

                            <tr>
                                <th>USUARIO</th>
                                <th>CORREO</th>
                                <th>ACCIONES</th>
                            </tr>

                        </thead>


                        <tbody>

                            {usuariosFiltrados.length > 0 ? (

                                usuariosFiltrados.map((usuario) => (

                                    <tr key={usuario.id}>

                                        <td>
                                            {usuario.nombre}
                                        </td>

                                        <td>
                                            {usuario.correo}
                                        </td>

                                        <td>

                                            <button
                                                className="btn btn-warning btn-sm me-2"
                                                type="button"
                                            >
                                                Editar
                                            </button>

                                            <button
                                                className="btn btn-danger btn-sm"
                                                type="button"
                                                onClick={() =>
                                                    eliminarUsuario(usuario.id)
                                                }
                                            >
                                                Eliminar
                                            </button>

                                        </td>

                                    </tr>

                                ))

                            ) : (

                                <tr>

                                    <td
                                        colSpan="3"
                                        className="sin-resultados"
                                    >
                                        No se encontraron usuarios.
                                    </td>

                                </tr>

                            )}

                        </tbody>

                    </table>

                </div>

            </div>

        </div>
    );
}

export default Usuarios;