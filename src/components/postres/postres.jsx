import { useEffect, useState } from "react";
import api from "../../api/axios";
import "./postres.css";

function Postres() {
    const [postres, setPostres] = useState([]);
    const [recetas, setRecetas] = useState([]);

    const [nombre, setNombre] = useState("");
    const [precio, setPrecio] = useState("");
    const [idReceta, setIdReceta] = useState("");

    const [mostrarFormulario, setMostrarFormulario] = useState(false);
    const [editando, setEditando] = useState(null);

    useEffect(() => {
        cargarPostres();
        cargarRecetas();
    }, []);

    async function cargarPostres() {
        try {
            const respuesta = await api.get("/postres/");
            setPostres(respuesta.data);
        } catch (error) {
            console.error("Error al cargar postres:", error);
        }
    }

    async function cargarRecetas() {
        try {
            const respuesta = await api.get("/recetas/");
            setRecetas(respuesta.data);
        } catch (error) {
            console.error("Error al cargar recetas:", error);
        }
    }

    function limpiarFormulario() {
        setNombre("");
        setPrecio("");
        setIdReceta("");
        setEditando(null);
    }

    function abrirNuevo() {
        limpiarFormulario();
        setMostrarFormulario(true);
    }

    function cancelar() {
        limpiarFormulario();
        setMostrarFormulario(false);
    }

    function editarPostre(postre) {
        setEditando(postre.id_postre);
        setNombre(postre.nombre);
        setPrecio(postre.precio);
        setIdReceta(postre.id_receta);
        setMostrarFormulario(true);
    }

    async function guardarPostre(evento) {
        evento.preventDefault();

        if (
            nombre.trim() === "" ||
            precio === "" ||
            idReceta === ""
        ) {
            alert("Completa todos los campos.");
            return;
        }

        if (Number(precio) < 0) {
            alert("El precio no puede ser negativo.");
            return;
        }

        const datos = {
            id_receta: Number(idReceta),
            nombre: nombre.trim(),
            precio: Number(precio),
            imagen: null,
        };

        try {
            if (editando) {
                const respuesta = await api.put(
                    `/postres/${editando}`,
                    datos
                );

                setPostres(
                    postres.map((postre) =>
                        postre.id_postre === editando
                            ? respuesta.data
                            : postre
                    )
                );
            } else {
                const respuesta = await api.post(
                    "/postres/",
                    datos
                );

                setPostres([...postres, respuesta.data]);
            }

            cancelar();
        } catch (error) {
            console.error("Error al guardar postre:", error);

            if (error.response && error.response.data) {
                alert(
                    error.response.data.detail ||
                    "No se pudo guardar el postre."
                );
            } else {
                alert("No se pudo guardar el postre.");
            }
        }
    }

    async function eliminarPostre(idPostre) {
        const confirmar = window.confirm(
            "¿Deseas eliminar este postre?"
        );

        if (!confirmar) {
            return;
        }

        try {
            await api.delete(`/postres/${idPostre}`);

            setPostres(
                postres.filter(
                    (postre) =>
                        postre.id_postre !== idPostre
                )
            );
        } catch (error) {
            console.error("Error al eliminar postre:", error);

            if (error.response && error.response.data) {
                alert(
                    error.response.data.detail ||
                    "No se pudo eliminar el postre."
                );
            } else {
                alert("No se pudo eliminar el postre.");
            }
        }
    }

    function obtenerNombreReceta(idRecetaPostre) {
        const receta = recetas.find(
            (item) =>
                item.id_receta === idRecetaPostre
        );

        if (!receta) {
            return "Sin receta";
        }

        return receta.nombre;
    }

    return (
        <div className="postres-container">

            <div className="postres-header">

                <div>
                    <h2>Postres</h2>
                    <p>Gestion de postres</p>
                </div>

                {!mostrarFormulario && (
                    <button
                        className="btn-nuevo-postre"
                        onClick={abrirNuevo}
                    >
                        + Nuevo Postre
                    </button>
                )}

            </div>

            {mostrarFormulario && (
                <div className="postre-formulario">

                    <div className="formulario-titulo">
                        <h3>
                            {editando
                                ? "Editar Postre"
                                : "Nuevo Postre"}
                        </h3>
                    </div>

                    <form onSubmit={guardarPostre}>

                        <div className="formulario-grid">

                            <div className="campo">

                                <label>Nombre</label>

                                <input
                                    type="text"
                                    value={nombre}
                                    onChange={(evento) =>
                                        setNombre(evento.target.value)
                                    }
                                    placeholder="Ej. Torta de Chocolate"
                                />

                            </div>

                            <div className="campo">

                                <label>Precio</label>

                                <div className="campo-precio">

                                    <span>S/</span>

                                    <input
                                        type="number"
                                        min="0"
                                        step="0.01"
                                        value={precio}
                                        onChange={(evento) =>
                                            setPrecio(evento.target.value)
                                        }
                                        placeholder="0.00"
                                    />

                                </div>

                            </div>

                            <div className="campo">

                                <label>Receta</label>

                                <select
                                    value={idReceta}
                                    onChange={(evento) =>
                                        setIdReceta(evento.target.value)
                                    }
                                >

                                    <option value="">
                                        Seleccionar receta
                                    </option>

                                    {recetas.map((receta) => (
                                        <option
                                            key={receta.id_receta}
                                            value={receta.id_receta}
                                        >
                                            {receta.nombre}
                                        </option>
                                    ))}

                                </select>

                            </div>

                        </div>

                        <div className="formulario-nota">
                            La imagen se mantiene en la base de datos
                            para el Catalogo Publico.
                        </div>

                        <div className="formulario-botones">

                            <button
                                type="submit"
                                className="btn-guardar-postre"
                            >
                                {editando
                                    ? "Actualizar"
                                    : "Crear"}
                            </button>

                            <button
                                type="button"
                                className="btn-cancelar-postre"
                                onClick={cancelar}
                            >
                                Cancelar
                            </button>

                        </div>

                    </form>

                </div>
            )}

            <div className="postres-tabla">

                <div className="tabla-titulo">
                    <h3>Lista de Postres</h3>
                </div>

                <div className="tabla-contenedor">

                    <table>

                        <thead>
                            <tr>
                                <th>Imagen</th>
                                <th>Nombre</th>
                                <th>Receta</th>
                                <th>Precio</th>
                                <th>Acciones</th>
                            </tr>
                        </thead>

                        <tbody>

                            {postres.length === 0 ? (

                                <tr>

                                    <td
                                        colSpan="5"
                                        className="tabla-vacia"
                                    >
                                        No hay postres registrados.
                                    </td>

                                </tr>

                            ) : (

                                postres.map((postre) => (

                                    <tr
                                        key={postre.id_postre}
                                    >

                                        <td>

                                            {postre.imagen ? (
                                                <span className="imagen-nombre">
                                                    {postre.imagen}
                                                </span>
                                            ) : (
                                                <span className="sin-imagen">
                                                    Sin imagen
                                                </span>
                                            )}

                                        </td>

                                        <td>
                                            {postre.nombre}
                                        </td>

                                        <td>
                                            {obtenerNombreReceta(
                                                postre.id_receta
                                            )}
                                        </td>

                                        <td>
                                            S/{" "}
                                            {Number(
                                                postre.precio
                                            ).toFixed(2)}
                                        </td>

                                        <td className="acciones">

                                            <button
                                                className="btn-editar-postre"
                                                onClick={() =>
                                                    editarPostre(postre)
                                                }
                                            >
                                                Editar
                                            </button>

                                            <button
                                                className="btn-eliminar-postre"
                                                onClick={() =>
                                                    eliminarPostre(
                                                        postre.id_postre
                                                    )
                                                }
                                            >
                                                Eliminar
                                            </button>

                                        </td>

                                    </tr>

                                ))

                            )}

                        </tbody>

                    </table>

                </div>

            </div>

        </div>
    );
}

export default Postres;