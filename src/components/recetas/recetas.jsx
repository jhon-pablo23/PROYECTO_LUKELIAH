import { useEffect, useState } from "react";
import api from "../../api/axios";
import "./recetas.css";

function Recetas() {
    const [recetas, setRecetas] = useState([]);
    const [ingredientes, setIngredientes] = useState([]);
    const [ingredientesReceta, setIngredientesReceta] = useState([]);

    const [nombre, setNombre] = useState("");
    const [porciones, setPorciones] = useState("");
    const [procedimiento, setProcedimiento] = useState("");

    const [ingredienteSeleccionado, setIngredienteSeleccionado] = useState("");
    const [cantidad, setCantidad] = useState("");

    const [mostrarFormulario, setMostrarFormulario] = useState(false);
    const [editando, setEditando] = useState(null);

    useEffect(() => {
        cargarRecetas();
        cargarIngredientes();
    }, []);

    async function cargarRecetas() {
        try {
            const respuesta = await api.get("/recetas/");
            setRecetas(respuesta.data);
        } catch (error) {
            console.error("Error al cargar recetas:", error);
        }
    }

    async function cargarIngredientes() {
        try {
            const respuesta = await api.get("/ingredientes/");
            setIngredientes(respuesta.data);
        } catch (error) {
            console.error("Error al cargar ingredientes:", error);
        }
    }

    async function cargarIngredientesReceta(idReceta) {
        try {
            const respuesta = await api.get(
                `/recetas/${idReceta}/ingredientes`
            );

            setIngredientesReceta(respuesta.data);
        } catch (error) {
            console.error(
                "Error al cargar ingredientes de la receta:",
                error
            );

            setIngredientesReceta([]);
        }
    }

    function limpiarFormulario() {
        setNombre("");
        setPorciones("");
        setProcedimiento("");
        setIngredienteSeleccionado("");
        setCantidad("");
        setIngredientesReceta([]);
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

    async function editarReceta(receta) {
        setEditando(receta.id_receta);
        setNombre(receta.nombre);
        setPorciones(receta.porciones);
        setProcedimiento(receta.procedimiento);
        setMostrarFormulario(true);

        await cargarIngredientesReceta(receta.id_receta);
    }

    async function guardarReceta(evento) {
        evento.preventDefault();

        if (
            nombre.trim() === "" ||
            porciones === "" ||
            procedimiento.trim() === ""
        ) {
            alert("Completa todos los campos.");
            return;
        }

        if (Number(porciones) <= 0) {
            alert("Las porciones deben ser mayores a 0.");
            return;
        }

        const datos = {
            nombre: nombre.trim(),
            porciones: Number(porciones),
            procedimiento: procedimiento.trim(),
        };

        try {
            if (editando) {
                const respuesta = await api.put(
                    `/recetas/${editando}`,
                    datos
                );

                setRecetas(
                    recetas.map((receta) =>
                        receta.id_receta === editando
                            ? respuesta.data
                            : receta
                    )
                );

                alert("Receta actualizada correctamente.");
            } else {
                const respuesta = await api.post(
                    "/recetas/",
                    datos
                );

                setRecetas([...recetas, respuesta.data]);

                setEditando(respuesta.data.id_receta);

                setNombre(respuesta.data.nombre);
                setPorciones(respuesta.data.porciones);
                setProcedimiento(respuesta.data.procedimiento);

                await cargarIngredientesReceta(
                    respuesta.data.id_receta
                );

                alert(
                    "Receta creada. Ahora puedes agregar ingredientes."
                );

                return;
            }

            cancelar();
        } catch (error) {
            console.error("Error al guardar receta:", error);

            if (error.response && error.response.data) {
                alert(
                    error.response.data.detail ||
                    "No se pudo guardar la receta."
                );
            } else {
                alert("No se pudo guardar la receta.");
            }
        }
    }

    async function agregarIngrediente() {
        if (!editando) {
            alert("Primero debes guardar la receta.");
            return;
        }

        if (ingredienteSeleccionado === "") {
            alert("Selecciona un ingrediente.");
            return;
        }

        if (cantidad === "") {
            alert("Ingresa la cantidad.");
            return;
        }

        if (Number(cantidad) <= 0) {
            alert("La cantidad debe ser mayor a 0.");
            return;
        }

        const datos = {
            id_receta: editando,
            id_ingrediente: Number(ingredienteSeleccionado),
            cantidad: Number(cantidad),
        };

        try {
            await api.post(
                `/recetas/${editando}/ingredientes`,
                datos
            );

            await cargarIngredientesReceta(editando);

            setIngredienteSeleccionado("");
            setCantidad("");
        } catch (error) {
            console.error(
                "Error al agregar ingrediente:",
                error
            );

            if (error.response && error.response.data) {
                alert(
                    error.response.data.detail ||
                    "No se pudo agregar el ingrediente."
                );
            } else {
                alert("No se pudo agregar el ingrediente.");
            }
        }
    }

    async function eliminarIngrediente(idIngrediente) {
        const confirmar = window.confirm(
            "¿Deseas eliminar este ingrediente de la receta?"
        );

        if (!confirmar) {
            return;
        }

        try {
            await api.delete(
                `/recetas/${editando}/ingredientes/${idIngrediente}`
            );

            await cargarIngredientesReceta(editando);
        } catch (error) {
            console.error(
                "Error al eliminar ingrediente:",
                error
            );

            if (error.response && error.response.data) {
                alert(
                    error.response.data.detail ||
                    "No se pudo eliminar el ingrediente."
                );
            } else {
                alert("No se pudo eliminar el ingrediente.");
            }
        }
    }

    async function eliminarReceta(idReceta) {
        const confirmar = window.confirm(
            "¿Deseas eliminar esta receta?"
        );

        if (!confirmar) {
            return;
        }

        try {
            await api.delete(`/recetas/${idReceta}`);

            setRecetas(
                recetas.filter(
                    (receta) => receta.id_receta !== idReceta
                )
            );

            if (editando === idReceta) {
                cancelar();
            }
        } catch (error) {
            console.error("Error al eliminar receta:", error);

            if (error.response && error.response.data) {
                alert(
                    error.response.data.detail ||
                    "No se pudo eliminar la receta."
                );
            } else {
                alert("No se pudo eliminar la receta.");
            }
        }
    }

    function obtenerUnidad(idIngrediente) {
        const ingrediente = ingredientes.find(
            (item) =>
                item.id_ingrediente === idIngrediente
        );

        if (!ingrediente) {
            return "";
        }

        return ingrediente.unidad_medida;
    }

    return (
        <div className="recetas-container">

            <div className="recetas-header">

                <div>
                    <h2>Recetas</h2>
                    <p>Gestion de recetas</p>
                </div>

                {!mostrarFormulario && (
                    <button
                        className="btn-nueva-receta"
                        onClick={abrirNuevo}
                    >
                        + Nueva Receta
                    </button>
                )}

            </div>

            {mostrarFormulario && (
                <div className="receta-formulario">

                    <div className="formulario-titulo">
                        <h3>
                            {editando
                                ? "Editar Receta"
                                : "Nueva Receta"}
                        </h3>
                    </div>

                    <form onSubmit={guardarReceta}>

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
                                <label>Porciones</label>

                                <input
                                    type="number"
                                    min="1"
                                    value={porciones}
                                    onChange={(evento) =>
                                        setPorciones(evento.target.value)
                                    }
                                    placeholder="Ej. 12"
                                />
                            </div>

                        </div>

                        <div className="campo procedimiento-campo">

                            <label>Procedimiento</label>

                            <textarea
                                value={procedimiento}
                                onChange={(evento) =>
                                    setProcedimiento(evento.target.value)
                                }
                                placeholder="Describe el procedimiento de la receta"
                                rows="4"
                            />

                        </div>

                        <div className="ingredientes-seccion">

                            <h4>Ingredientes</h4>

                            <div className="ingrediente-agregar">

                                <div className="campo">

                                    <label>Ingrediente</label>

                                    <select
                                        value={ingredienteSeleccionado}
                                        onChange={(evento) =>
                                            setIngredienteSeleccionado(
                                                evento.target.value
                                            )
                                        }
                                    >
                                        <option value="">
                                            Seleccionar ingrediente
                                        </option>

                                        {ingredientes.map((ingrediente) => (
                                            <option
                                                key={ingrediente.id_ingrediente}
                                                value={ingrediente.id_ingrediente}
                                            >
                                                {ingrediente.nombre}
                                            </option>
                                        ))}

                                    </select>

                                </div>

                                <div className="campo">

                                    <label>Cantidad</label>

                                    <input
                                        type="number"
                                        min="0.01"
                                        step="0.01"
                                        value={cantidad}
                                        onChange={(evento) =>
                                            setCantidad(evento.target.value)
                                        }
                                        placeholder="Ej. 500"
                                    />

                                </div>

                                <div className="boton-agregar-contenedor">

                                    <button
                                        type="button"
                                        className="btn-agregar-ingrediente"
                                        onClick={agregarIngrediente}
                                    >
                                        Agregar ingrediente
                                    </button>

                                </div>

                            </div>

                            <div className="ingredientes-lista">

                                {ingredientesReceta.length === 0 ? (

                                    <div className="sin-ingredientes">
                                        No hay ingredientes agregados.
                                    </div>

                                ) : (

                                    <table>

                                        <thead>
                                            <tr>
                                                <th>Ingrediente</th>
                                                <th>Cantidad</th>
                                                <th>Accion</th>
                                            </tr>
                                        </thead>

                                        <tbody>

                                            {ingredientesReceta.map(
                                                (ingrediente) => (

                                                    <tr
                                                        key={
                                                            ingrediente.id_ingrediente
                                                        }
                                                    >

                                                        <td>
                                                            {ingrediente.nombre}
                                                        </td>

                                                        <td>
                                                            {Number(
                                                                ingrediente.cantidad
                                                            ).toFixed(2)}{" "}
                                                            {ingrediente.unidad_medida ||
                                                                obtenerUnidad(
                                                                    ingrediente.id_ingrediente
                                                                )}
                                                        </td>

                                                        <td>

                                                            <button
                                                                type="button"
                                                                className="btn-eliminar-ingrediente"
                                                                onClick={() =>
                                                                    eliminarIngrediente(
                                                                        ingrediente.id_ingrediente
                                                                    )
                                                                }
                                                            >
                                                                Eliminar
                                                            </button>

                                                        </td>

                                                    </tr>

                                                )
                                            )}

                                        </tbody>

                                    </table>

                                )}

                            </div>

                        </div>

                        <div className="formulario-botones">

                            <button
                                type="submit"
                                className="btn-guardar-receta"
                            >
                                {editando
                                    ? "Actualizar"
                                    : "Crear"}
                            </button>

                            <button
                                type="button"
                                className="btn-cancelar-receta"
                                onClick={cancelar}
                            >
                                Cancelar
                            </button>

                        </div>

                    </form>

                </div>
            )}

            <div className="recetas-tabla">

                <div className="tabla-titulo">
                    <h3>Lista de Recetas</h3>
                </div>

                <div className="tabla-contenedor">

                    <table>

                        <thead>
                            <tr>
                                <th>Nombre</th>
                                <th>Porciones</th>
                                <th>Procedimiento</th>
                                <th>Acciones</th>
                            </tr>
                        </thead>

                        <tbody>

                            {recetas.length === 0 ? (

                                <tr>
                                    <td
                                        colSpan="4"
                                        className="tabla-vacia"
                                    >
                                        No hay recetas registradas.
                                    </td>
                                </tr>

                            ) : (

                                recetas.map((receta) => (

                                    <tr key={receta.id_receta}>

                                        <td>
                                            {receta.nombre}
                                        </td>

                                        <td>
                                            {receta.porciones}
                                        </td>

                                        <td className="procedimiento-tabla">
                                            {receta.procedimiento}
                                        </td>

                                        <td className="acciones">

                                            <button
                                                className="btn-editar-receta"
                                                onClick={() =>
                                                    editarReceta(receta)
                                                }
                                            >
                                                Editar
                                            </button>

                                            <button
                                                className="btn-eliminar-receta"
                                                onClick={() =>
                                                    eliminarReceta(
                                                        receta.id_receta
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

export default Recetas;