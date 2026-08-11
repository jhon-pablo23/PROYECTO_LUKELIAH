import { useEffect, useState } from "react";
import api from "../../api/axios";
import "./catalogo.css";

function Catalogo() {

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
                        key={postre.id_postre}
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
                                    S/ {Number(postre.precio).toFixed(2)}
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