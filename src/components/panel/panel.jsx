import "./panel.css";

function Panel() {
    return (
        <div className="panel">

            {/* Encabezado */}
            <div className="panel-header">
                <h1>Dashboard</h1>
                <p>Bienvenido a LUKELIAH</p>
            </div>

            {/* Tarjetas */}
            <div className="panel-cards">

                <div className="panel-card">
                    <div className="panel-card-icon">🧂</div>
                    <div>
                        <h2>8</h2>
                        <p>Ingredientes</p>
                    </div>
                </div>

                <div className="panel-card">
                    <div className="panel-card-icon">📖</div>
                    <div>
                        <h2>4</h2>
                        <p>Recetas</p>
                    </div>
                </div>

                <div className="panel-card">
                    <div className="panel-card-icon">🍰</div>
                    <div>
                        <h2>6</h2>
                        <p>Postres</p>
                    </div>
                </div>

                <div className="panel-card">
                    <div className="panel-card-icon">🛒</div>
                    <div>
                        <h2>7</h2>
                        <p>Ventas</p>
                    </div>
                </div>

                <div className="panel-card">
                    <div className="panel-card-icon">⚠️</div>
                    <div>
                        <h2>2</h2>
                        <p>Stock Crítico</p>
                    </div>
                </div>

            </div>

            {/* Ultimas ventas */}
            <div className="ventas-panel">

                <h2>Últimas ventas</h2>

                <div className="tabla-container">

                    <table className="tabla-ventas">

                        <thead>
                            <tr>
                                <th>FECHA</th>
                                <th>POSTRE</th>
                                <th>CANTIDAD</th>
                                <th>TOTAL</th>
                            </tr>
                        </thead>

                        <tbody>

                            <tr>
                                <td>2026-07-10</td>
                                <td>Tiramisú Italiano</td>
                                <td>1</td>
                                <td>S/ 45.00</td>
                            </tr>

                            <tr>
                                <td>2026-07-10</td>
                                <td>Torta de Chocolate Premium</td>
                                <td>1</td>
                                <td>S/ 65.00</td>
                            </tr>

                            <tr>
                                <td>2026-07-10</td>
                                <td>Torta de Chocolate Premium</td>
                                <td>2</td>
                                <td>S/ 130.00</td>
                            </tr>

                            <tr>
                                <td>2026-07-10</td>
                                <td>Cheesecake de Frutos Rojos</td>
                                <td>1</td>
                                <td>S/ 55.00</td>
                            </tr>

                            <tr>
                                <td>2026-07-09</td>
                                <td>Brownie con Helado</td>
                                <td>5</td>
                                <td>S/ 90.00</td>
                            </tr>

                        </tbody>

                    </table>

                </div>

            </div>

        </div>
    );
}

export default Panel;