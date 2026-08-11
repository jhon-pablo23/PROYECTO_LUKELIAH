import { useEffect, useState } from "react";
import api from "../../api/axios";
import "./panel.css";

function Panel() {

    const [cantidadIngredientes, setCantidadIngredientes] = useState(0);
    const [cantidadRecetas, setCantidadRecetas] = useState(0);
    const [cantidadPostres, setCantidadPostres] = useState(0);
    const [cantidadVentas, setCantidadVentas] = useState(0);
    const [stockCritico, setStockCritico] = useState(0);

    const [ultimasVentas, setUltimasVentas] = useState([]);

    useEffect(() => {
        cargarDashboard();
    }, []);

    async function cargarDashboard() {

        try {

            const respuestaIngredientes = await api.get(
                "/ingredientes/"
            );

            const respuestaRecetas = await api.get(
                "/recetas/"
            );

            const respuestaPostres = await api.get(
                "/postres/"
            );

            const respuestaVentas = await api.get(
                "/ventas/"
            );


            // INGREDIENTES

            const ingredientes = respuestaIngredientes.data;

            setCantidadIngredientes(
                ingredientes.length
            );


            // STOCK CRITICO

            const ingredientesCriticos = ingredientes.filter(
                (ingrediente) =>
                    Number(ingrediente.stock_actual) <=
                    Number(ingrediente.stock_minimo)
            );

            setStockCritico(
                ingredientesCriticos.length
            );


            // RECETAS

            setCantidadRecetas(
                respuestaRecetas.data.length
            );


            // POSTRES

            setCantidadPostres(
                respuestaPostres.data.length
            );


            // VENTAS

            const ventas = respuestaVentas.data;

            setCantidadVentas(
                ventas.length
            );


            // ULTIMAS VENTAS

            const ventasOrdenadas = [...ventas].reverse();

            const ventasMostrar = [];

            ventasOrdenadas.forEach((venta) => {

                if (venta.detalle) {

                    venta.detalle.forEach((detalle) => {

                        ventasMostrar.push({
                            fecha: venta.fecha,
                            nombre: detalle.nombre,
                            cantidad: detalle.cantidad,
                            total: detalle.subtotal
                        });

                    });

                }

            });

            setUltimasVentas(
                ventasMostrar.slice(0, 5)
            );

        } catch (error) {

            console.error(
                "Error al cargar el Dashboard:",
                error
            );

        }

    }


    return (

        <div className="panel">


            {/* ENCABEZADO */}

            <div className="panel-header">

                <h1>
                    Dashboard
                </h1>

                <p>
                    Bienvenido a LUKELIAH
                </p>

            </div>


            {/* TARJETAS */}

            <div className="panel-cards">


                {/* INGREDIENTES */}

                <div className="panel-card">

                    <div className="panel-card-icon">
                        🧂
                    </div>

                    <div>

                        <h2>
                            {cantidadIngredientes}
                        </h2>

                        <p>
                            Ingredientes
                        </p>

                    </div>

                </div>


                {/* RECETAS */}

                <div className="panel-card">

                    <div className="panel-card-icon">
                        📖
                    </div>

                    <div>

                        <h2>
                            {cantidadRecetas}
                        </h2>

                        <p>
                            Recetas
                        </p>

                    </div>

                </div>


                {/* POSTRES */}

                <div className="panel-card">

                    <div className="panel-card-icon">
                        🍰
                    </div>

                    <div>

                        <h2>
                            {cantidadPostres}
                        </h2>

                        <p>
                            Postres
                        </p>

                    </div>

                </div>


                {/* VENTAS */}

                <div className="panel-card">

                    <div className="panel-card-icon">
                        🛒
                    </div>

                    <div>

                        <h2>
                            {cantidadVentas}
                        </h2>

                        <p>
                            Ventas
                        </p>

                    </div>

                </div>


                {/* STOCK CRITICO */}

                <div className="panel-card">

                    <div className="panel-card-icon">
                        ⚠️
                    </div>

                    <div>

                        <h2>
                            {stockCritico}
                        </h2>

                        <p>
                            Stock Crítico
                        </p>

                    </div>

                </div>

            </div>


            {/* ULTIMAS VENTAS */}

            <div className="ventas-panel">

                <h2>
                    Últimas ventas
                </h2>


                <div className="tabla-container">

                    <table className="tabla-ventas">

                        <thead>

                            <tr>

                                <th>
                                    FECHA
                                </th>

                                <th>
                                    POSTRE
                                </th>

                                <th>
                                    CANTIDAD
                                </th>

                                <th>
                                    TOTAL
                                </th>

                            </tr>

                        </thead>


                        <tbody>

                            {ultimasVentas.length === 0 ? (

                                <tr>

                                    <td
                                        colSpan="4"
                                        style={{
                                            textAlign: "center"
                                        }}
                                    >
                                        No hay ventas registradas.
                                    </td>

                                </tr>

                            ) : (

                                ultimasVentas.map(
                                    (venta, index) => (

                                        <tr key={index}>

                                            <td>
                                                {venta.fecha}
                                            </td>

                                            <td>
                                                {venta.nombre}
                                            </td>

                                            <td>
                                                {venta.cantidad}
                                            </td>

                                            <td>
                                                S/ {Number(
                                                    venta.total
                                                ).toFixed(2)}
                                            </td>

                                        </tr>

                                    )
                                )

                            )}

                        </tbody>

                    </table>

                </div>

            </div>

        </div>

    );

}

export default Panel;