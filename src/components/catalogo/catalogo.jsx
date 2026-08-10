import "./catalogo.css";

function Catalogo() {

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
        },
        {
            id: 4,
            nombre: "Torta de Fresa",
            precio: 55.00
        }
    ];

    return (
        <div className="catalogo-container">

            {/* TITULO */}

            <div className="catalogo-header">

                <h1>
                    Catálogo Público
                </h1>

                <p>
                    Conoce nuestros postres disponibles
                </p>

            </div>


            {/* TARJETAS */}

            <div className="row g-4">

                {postres.map((postre) => (

                    <div
                        className="col-md-6 col-lg-4 col-xl-3"
                        key={postre.id}
                    >

                        <div className="catalogo-card">

                            {/* IMAGEN */}

                            <div className="catalogo-imagen">

                                <span>
                                    Imagen
                                </span>

                            </div>


                            {/* INFORMACION */}

                            <div className="catalogo-info">

                                <h5>
                                    {postre.nombre}
                                </h5>

                                <p>
                                    S/ {postre.precio.toFixed(2)}
                                </p>

                            </div>

                        </div>

                    </div>

                ))}

            </div>

        </div>
    );
}

export default Catalogo;