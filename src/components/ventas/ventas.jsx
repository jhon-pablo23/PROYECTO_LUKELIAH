import { useEffect, useState } from "react";
import api from "../../api/axios";
import "./ventas.css";

function Ventas() {

    const [fecha, setFecha] = useState("2026-07-10");
    const [postreSeleccionado, setPostreSeleccionado] = useState("");
    const [cantidad, setCantidad] = useState(1);
    const [postres, setPostres] = useState([]);

    useEffect(() => {
        cargarPostres();
    }, []);

    async function cargarPostres() {
        try {
            const respuesta = await api.get("/postres/");
            setPostres(respuesta.data);
        } catch (error) {
            console.error("Error al cargar postres:", error);
        }
    }

    const postre = postres.find(
        (p) => p.id_postre === Number(postreSeleccionado)
    );

    const precioUnitario = postre ? Number(postre.precio) : 0;

    const total = precioUnitario * Number(cantidad);

    function registrarVenta() {

        if (postreSeleccionado === "") {
            alert("Seleccione un postre.");
            return;
        }

        if (cantidad <= 0) {
            alert("La cantidad debe ser mayor que cero.");
            return;
        }

        alert("Venta registrada correctamente.");
    }

    return (
        <div className="ventas-container">

            {/* TITULO */}

            <div className="ventas-header">

                <div>
                    <h1>Registrar Venta</h1>
                </div>

            </div>


            {/* CONTENIDO PRINCIPAL */}

            <div className="row g-4">


                {/* FORMULARIO */}

                <div className="col-lg-8">

                    <div className="ventas-card">

                        <div className="row">


                            {/* FECHA */}

                            <div className="col-md-6 mb-3">

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


                            {/* USUARIO */}

                            <div className="col-md-6 mb-3">

                                <label className="form-label">
                                    Usuario
                                </label>

                                <input
                                    type="text"
                                    className="form-control"
                                    value="JHON EMERSON ANCHAYHUA PABLO"
                                    readOnly
                                />

                            </div>


                            {/* POSTRE */}

                            <div className="col-md-8 mb-3">

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
                                        Seleccionar postre...
                                    </option>

                                    {postres.map((postre) => (
                                        <option
                                            key={postre.id_postre}
                                            value={postre.id_postre}
                                        >
                                            {postre.nombre}
                                        </option>
                                    ))}

                                </select>

                            </div>


                            {/* CANTIDAD */}

                            <div className="col-md-4 mb-3">

                                <label className="form-label">
                                    Cantidad
                                </label>

                                <input
                                    type="number"
                                    className="form-control"
                                    min="1"
                                    value={cantidad}
                                    onChange={(e) =>
                                        setCantidad(Number(e.target.value))
                                    }
                                />

                            </div>


                            {/* BOTON */}

                            <div className="col-12">

                                <button
                                    type="button"
                                    className="ventas-btn-registrar"
                                    onClick={registrarVenta}
                                    disabled={!postreSeleccionado}
                                >
                                    Registrar Venta
                                </button>

                            </div>

                        </div>

                    </div>

                </div>


                {/* RESUMEN */}

                <div className="col-lg-4">

                    <div className="ventas-card ventas-resumen">

                        <h6>RESUMEN</h6>


                        <div className="resumen-fila">

                            <span>Postre</span>

                            <strong>
                                {postre
                                    ? postre.nombre
                                    : "—"}
                            </strong>

                        </div>


                        <div className="resumen-fila">

                            <span>Cantidad</span>

                            <strong>
                                {cantidad}
                            </strong>

                        </div>


                        <div className="resumen-fila">

                            <span>Precio unit.</span>

                            <strong>
                                S/ {precioUnitario.toFixed(2)}
                            </strong>

                        </div>


                        <div className="resumen-total">

                            <span>
                                Total
                            </span>

                            <strong>
                                S/ {total.toFixed(2)}
                            </strong>

                        </div>

                    </div>

                </div>

            </div>

        </div>
    );
}

export default Ventas;