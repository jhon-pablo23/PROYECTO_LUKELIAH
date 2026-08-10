import { useEffect, useState } from "react";
import api from "../../api/axios";
import "./ingredientes.css";

function Ingredientes() {
    const [ingredientes, setIngredientes] = useState([]);

    const [nombre, setNombre] = useState("");
    const [unidadMedida, setUnidadMedida] = useState("kg");
    const [stockActual, setStockActual] = useState("");
    const [stockMinimo, setStockMinimo] = useState("");
    const [costo, setCosto] = useState("");

    const [mostrarFormulario, setMostrarFormulario] = useState(false);
    const [editando, setEditando] = useState(null);

    useEffect(() => {
        cargarIngredientes();
    }, []);

    async function cargarIngredientes() {
        try {
            const respuesta = await api.get("/ingredientes/");
            setIngredientes(respuesta.data);
        } catch (error) {
            console.error("Error al cargar ingredientes:", error);
        }
    }

    function limpiarFormulario() {
        setNombre("");
        setUnidadMedida("kg");
        setStockActual("");
        setStockMinimo("");
        setCosto("");
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

    function editarIngrediente(ingrediente) {
        setEditando(ingrediente.id_ingrediente);
        setNombre(ingrediente.nombre);
        setUnidadMedida(ingrediente.unidad_medida);
        setStockActual(ingrediente.stock_actual);
        setStockMinimo(ingrediente.stock_minimo);
        setCosto(ingrediente.costo);
        setMostrarFormulario(true);
    }

    async function guardarIngrediente(evento) {
        evento.preventDefault();

        if (
            nombre.trim() === "" ||
            stockActual === "" ||
            stockMinimo === "" ||
            costo === ""
        ) {
            alert("Completa todos los campos.");
            return;
        }

        if (
            Number(stockActual) < 0 ||
            Number(stockMinimo) < 0 ||
            Number(costo) < 0
        ) {
            alert("No se permiten valores negativos.");
            return;
        }

        const datos = {
            nombre: nombre.trim(),
            unidad_medida: unidadMedida,
            stock_actual: Number(stockActual),
            stock_minimo: Number(stockMinimo),
            costo: Number(costo),
        };

        try {
            if (editando) {
                const respuesta = await api.put(
                    `/ingredientes/${editando}`,
                    datos
                );

                setIngredientes(
                    ingredientes.map((ingrediente) =>
                        ingrediente.id_ingrediente === editando
                            ? respuesta.data
                            : ingrediente
                    )
                );
            } else {
                const respuesta = await api.post(
                    "/ingredientes/",
                    datos
                );

                setIngredientes([...ingredientes, respuesta.data]);
            }

            cancelar();
        } catch (error) {
            console.error("Error al guardar ingrediente:", error);

            if (error.response && error.response.data) {
                alert(
                    error.response.data.detail ||
                    "No se pudo guardar el ingrediente."
                );
            } else {
                alert("No se pudo guardar el ingrediente.");
            }
        }
    }

    async function eliminarIngrediente(id) {
        const confirmar = window.confirm(
            "¿Deseas eliminar este ingrediente?"
        );

        if (!confirmar) {
            return;
        }

        try {
            await api.delete(`/ingredientes/${id}`);

            setIngredientes(
                ingredientes.filter(
                    (ingrediente) =>
                        ingrediente.id_ingrediente !== id
                )
            );
        } catch (error) {
            console.error("Error al eliminar ingrediente:", error);

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

    return (
        <div className="ingredientes-container">

            <div className="ingredientes-header">
                <div>
                    <h2>Ingredientes</h2>
                    <p>Gestion de ingredientes</p>
                </div>

                {!mostrarFormulario && (
                    <button
                        className="btn-nuevo-ingrediente"
                        onClick={abrirNuevo}
                    >
                        + Nuevo Ingrediente
                    </button>
                )}
            </div>

            {mostrarFormulario && (
                <div className="ingrediente-formulario">

                    <div className="formulario-titulo">
                        <h3>
                            {editando
                                ? "Editar Ingrediente"
                                : "Nuevo Ingrediente"}
                        </h3>
                    </div>

                    <form onSubmit={guardarIngrediente}>

                        <div className="formulario-grid">

                            <div className="campo">
                                <label>Nombre</label>

                                <input
                                    type="text"
                                    value={nombre}
                                    onChange={(evento) =>
                                        setNombre(evento.target.value)
                                    }
                                    placeholder="Ej. Harina"
                                />
                            </div>

                            <div className="campo">
                                <label>Unidad de medida</label>

                                <select
                                    value={unidadMedida}
                                    onChange={(evento) =>
                                        setUnidadMedida(evento.target.value)
                                    }
                                >
                                    <option value="kg">kg</option>
                                    <option value="g">g</option>
                                    <option value="ml">ml</option>
                                    <option value="L">L</option>
                                    <option value="unidad">unidad</option>
                                </select>
                            </div>

                            <div className="campo">
                                <label>Stock actual</label>

                                <input
                                    type="number"
                                    min="0"
                                    step="0.01"
                                    value={stockActual}
                                    onChange={(evento) =>
                                        setStockActual(evento.target.value)
                                    }
                                    placeholder="Ej. 10"
                                />
                            </div>

                            <div className="campo">
                                <label>Stock minimo</label>

                                <input
                                    type="number"
                                    min="0"
                                    step="0.01"
                                    value={stockMinimo}
                                    onChange={(evento) =>
                                        setStockMinimo(evento.target.value)
                                    }
                                    placeholder="Ej. 2"
                                />
                            </div>

                            <div className="campo">
                                <label>Costo</label>

                                <div className="campo-precio">
                                    <span>S/</span>

                                    <input
                                        type="number"
                                        min="0"
                                        step="0.01"
                                        value={costo}
                                        onChange={(evento) =>
                                            setCosto(evento.target.value)
                                        }
                                        placeholder="0.00"
                                    />
                                </div>
                            </div>

                        </div>

                        <div className="formulario-botones">

                            <button
                                type="submit"
                                className="btn-guardar"
                            >
                                {editando ? "Actualizar" : "Crear"}
                            </button>

                            <button
                                type="button"
                                className="btn-cancelar"
                                onClick={cancelar}
                            >
                                Cancelar
                            </button>

                        </div>

                    </form>
                </div>
            )}

            <div className="ingredientes-tabla">

                <div className="tabla-titulo">
                    <h3>Lista de Ingredientes</h3>
                </div>

                <div className="tabla-contenedor">

                    <table>

                        <thead>
                            <tr>
                                <th>Nombre</th>
                                <th>Unidad</th>
                                <th>Stock</th>
                                <th>Stock minimo</th>
                                <th>Costo</th>
                                <th>Acciones</th>
                            </tr>
                        </thead>

                        <tbody>

                            {ingredientes.length === 0 ? (

                                <tr>
                                    <td
                                        colSpan="6"
                                        className="tabla-vacia"
                                    >
                                        No hay ingredientes registrados.
                                    </td>
                                </tr>

                            ) : (

                                ingredientes.map((ingrediente) => (

                                    <tr key={ingrediente.id_ingrediente}>

                                        <td>
                                            {ingrediente.nombre}
                                        </td>

                                        <td>
                                            {ingrediente.unidad_medida}
                                        </td>

                                        <td>
                                            {Number(
                                                ingrediente.stock_actual
                                            ).toFixed(2)}{" "}
                                            {ingrediente.unidad_medida}
                                        </td>

                                        <td>
                                            {Number(
                                                ingrediente.stock_minimo
                                            ).toFixed(2)}{" "}
                                            {ingrediente.unidad_medida}
                                        </td>

                                        <td>
                                            S/{" "}
                                            {Number(
                                                ingrediente.costo
                                            ).toFixed(2)}
                                        </td>

                                        <td className="acciones">

                                            <button
                                                className="btn-editar"
                                                onClick={() =>
                                                    editarIngrediente(
                                                        ingrediente
                                                    )
                                                }
                                            >
                                                Editar
                                            </button>

                                            <button
                                                className="btn-eliminar"
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

                                ))

                            )}

                        </tbody>

                    </table>

                </div>
            </div>

        </div>
    );
}

export default Ingredientes;