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

        <div className="catalogo">

            {/* ENCABEZADO */}

            <div className="catalogo-header d-flex justify-content-between align-items-center">

                <div>

                    <h1>
                        Catálogo Público
                    </h1>

                    <p>
                        Conoce nuestros postres disponibles
                    </p>

                </div>


                {/* BOTON DE WHATSAPP */}

                <a
                    href="https://wa.me/51912560956"
                    target="_blank"
                    rel="noreferrer"
                    className="btn btn-success"
                >
                    WhatsApp
                </a>

            </div>


            {/* TARJETAS */}

            <div className="row g-4">

                {postres.map((postre) => (

                    <div
                        className="col-md-6 col-lg-4 col-xl-3"
                        key={postre.id}
                    >

                        <div className="catalogo-card">

                            <div className="catalogo-imagen">

                                <span>
                                    Imagen
                                </span>

                            </div>

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