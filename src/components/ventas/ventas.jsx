import { useEffect, useState } from "react";
import "./ventas.css";
import api from "../../api/axios";

function Ventas() {

    const [fecha, setFecha] = useState("");
    const [postres, setPostres] = useState([]);
    const [postreSeleccionado, setPostreSeleccionado] = useState("");
    const [cantidad, setCantidad] = useState(1);
    const [guardando, setGuardando] = useState(false);

    // Cargar postres desde PostgreSQL
    useEffect(() => {

        api.get("/postres/")
            .then((respuesta) => {
                setPostres(respuesta.data);
            })
            .catch((error) => {
                console.error("Error al cargar postres:", error);
                alert("No se pudieron cargar los postres.");
            });

    }, []);

    const postre = postres.find(
        (p) => p.id_postre === Number(postreSeleccionado)
    );

    const precioUnitario = postre
        ? Number(postre.precio)
        : 0;

    const total = precioUnitario * Number(cantidad);

    function obtenerFechaActual() {

        const hoy = new Date();

        const anio = hoy.getFullYear();
        const mes = String(hoy.getMonth() + 1).padStart(2, "0");
        const dia = String(hoy.getDate()).padStart(2, "0");

        return `${anio}-${mes}-${dia}`;
    }

    async function registrarVenta() {

        if (postreSeleccionado === "") {
            alert("Seleccione un postre.");
            return;
        }

        if (Number(cantidad) <= 0) {
            alert("La cantidad debe ser mayor que cero.");
            return;
        }

        setGuardando(true);

        try {

            const datosVenta = {
                lineas: [
                    {
                        id_postre: Number(postreSeleccionado),
                        cantidad: Number(cantidad)
                    }
                ]
            };

            const respuesta = await api.post(
                "/ventas/",
                datosVenta
            );

            console.log("Venta registrada:", respuesta.data);

            setFecha(obtenerFechaActual());

            alert("Venta registrada correctamente.");

            setPostreSeleccionado("");
            setCantidad(1);

        } catch (error) {

            console.error("Error al registrar venta:", error);

            if (error.response) {
                console.error(
                    "Respuesta del servidor:",
                    error.response.data
                );

                alert(
                    "No se pudo registrar la venta: " +
                    JSON.stringify(error.response.data)
                );
            } else {
                alert(
                    "No se pudo conectar con el servidor."
                );
            }

        } finally {

            setGuardando(false);

        }
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
                                    value={fecha || obtenerFechaActual()}
                                    readOnly
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
                            <div className="col-12 mb-3">

                                <label className="form-label">
                                    Postre
                                </label>

                                <select
                                    className="form-select"
                                    value={postreSeleccionado}
                                    onChange={(e) =>
                                        setPostreSeleccionado(
                                            e.target.value
                                        )
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
                            <div className="col-md-6 mb-3">

                                <label className="form-label">
                                    Cantidad
                                </label>

                                <input
                                    type="number"
                                    min="1"
                                    className="form-control"
                                    value={cantidad}
                                    onChange={(e) =>
                                        setCantidad(
                                            Number(e.target.value)
                                        )
                                    }
                                />

                            </div>


                            {/* PRECIO UNITARIO */}
                            <div className="col-md-6 mb-3">

                                <label className="form-label">
                                    Precio unitario
                                </label>

                                <input
                                    type="text"
                                    className="form-control"
                                    value={
                                        postre
                                            ? `S/ ${precioUnitario.toFixed(2)}`
                                            : "—"
                                    }
                                    readOnly
                                />

                            </div>


                            {/* BOTON */}
                            <div className="col-12">

                                <button
                                    className="btn ventas-btn-registrar"
                                    onClick={registrarVenta}
                                    disabled={
                                        postreSeleccionado === "" ||
                                        guardando
                                    }
                                >

                                    {guardando
                                        ? "Guardando..."
                                        : "Registrar Venta"}

                                </button>

                            </div>

                        </div>

                    </div>

                </div>


                {/* RESUMEN */}
                <div className="col-lg-4">

                    <div className="ventas-card ventas-resumen">

                        <h6>
                            RESUMEN
                        </h6>


                        <div className="resumen-fila">

                            <span>
                                Postre
                            </span>

                            <strong>
                                {postre
                                    ? postre.nombre
                                    : "—"}
                            </strong>

                        </div>


                        <div className="resumen-fila">

                            <span>
                                Cantidad
                            </span>

                            <strong>
                                {cantidad}
                            </strong>

                        </div>


                        <div className="resumen-fila">

                            <span>
                                Precio unit.
                            </span>

                            <strong>
                                {postre
                                    ? `S/ ${precioUnitario.toFixed(2)}`
                                    : "—"}
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