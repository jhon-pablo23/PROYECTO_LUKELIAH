import { useState } from "react";
import "./ventas.css";

function Ventas() {
    const [fecha, setFecha] = useState("");
    const [postreSeleccionado, setPostreSeleccionado] = useState("");
    const [cantidad, setCantidad] = useState("");
    const [detalles, setDetalles] = useState([]);

    const postres = [
        {
            id: 1,
            nombre: "Torta de Chocolate",
            precio: 65.00
        },
        {
            id: 2,
            nombre: "Cheesecake",
            precio: 45.00
        },
        {
            id: 3,
            nombre: "Brownie",
            precio: 18.00
        }
    ];

    function agregarPostre() {
        if (postreSeleccionado === "") {
            alert("Seleccione un postre.");
            return;
        }

        if (cantidad === "" || Number(cantidad) <= 0) {
            alert("Ingrese una cantidad mayor que cero.");
            return;
        }

        const postre = postres.find(
            (p) => p.id === Number(postreSeleccionado)
        );

        const nuevoDetalle = {
            id: Date.now(),
            postre: postre.nombre,
            precio: postre.precio,
            cantidad: Number(cantidad),
            subtotal: postre.precio * Number(cantidad)
        };

        setDetalles([...detalles, nuevoDetalle]);

        setPostreSeleccionado("");
        setCantidad("");
    }

    function eliminarDetalle(id) {
        setDetalles(
            detalles.filter((detalle) => detalle.id !== id)
        );
    }

    const total = detalles.reduce(
        (suma, detalle) => suma + detalle.subtotal,
        0
    );

    return (
        <div className="ventas-container">

            <div className="ventas-header">
                <div>
                    <h1>Ventas</h1>
                    <p>Registro de ventas de postres</p>
                </div>
            </div>

            <div className="ventas-card">

                <h5>Registrar venta</h5>

                <div className="row">

                    <div className="col-md-4 mb-3">
                        <label className="form-label">
                            Fecha
                        </label>

                        <input
                            type="date"
                            className="form-control"
                            value={fecha}
                            onChange={(e) => setFecha(e.target.value)}
                        />
                    </div>

                </div>

                <hr />

                <h6>Agregar postre</h6>

                <div className="row align-items-end">

                    <div className="col-md-6 mb-3">
                        <label className="form-label">
                            Postre
                        </label>

                        <select
                            className="form-select"
                            value={postreSeleccionado}
                            onChange={(e) =>
                                setPostreSeleccionado(e.target.value)
                            }
                        >
                            <option value="">
                                Seleccione un postre
                            </option>

                            {postres.map((postre) => (
                                <option
                                    key={postre.id}
                                    value={postre.id}
                                >
                                    {postre.nombre} - S/ {postre.precio.toFixed(2)}
                                </option>
                            ))}
                        </select>
                    </div>

                    <div className="col-md-3 mb-3">
                        <label className="form-label">
                            Cantidad
                        </label>

                        <input
                            type="number"
                            min="1"
                            className="form-control"
                            value={cantidad}
                            onChange={(e) =>
                                setCantidad(e.target.value)
                            }
                        />
                    </div>

                    <div className="col-md-3 mb-3">
                        <button
                            className="btn btn-primary ventas-btn-agregar"
                            onClick={agregarPostre}
                        >
                            + Agregar
                        </button>
                    </div>

                </div>

            </div>

            <div className="ventas-card">

                <h5>Detalle de venta</h5>

                <div className="table-responsive">

                    <table className="table ventas-table">

                        <thead>
                            <tr>
                                <th>Postre</th>
                                <th>Cantidad</th>
                                <th>Subtotal</th>
                                <th>Acciones</th>
                            </tr>
                        </thead>

                        <tbody>

                            {detalles.length === 0 ? (

                                <tr>
                                    <td
                                        colSpan="4"
                                        className="ventas-vacio"
                                    >
                                        No hay postres agregados
                                    </td>
                                </tr>

                            ) : (

                                detalles.map((detalle) => (

                                    <tr key={detalle.id}>

                                        <td>
                                            {detalle.postre}
                                        </td>

                                        <td>
                                            {detalle.cantidad}
                                        </td>

                                        <td>
                                            S/ {detalle.subtotal.toFixed(2)}
                                        </td>

                                        <td>
                                            <button
                                                className="btn btn-sm btn-danger"
                                                onClick={() =>
                                                    eliminarDetalle(detalle.id)
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

                <div className="ventas-total">

                    <span>Total</span>

                    <strong>
                        S/ {total.toFixed(2)}
                    </strong>

                </div>

            </div>

        </div>
    );
}

export default Ventas;