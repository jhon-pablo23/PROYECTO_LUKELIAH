import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./login.css";

function Login() {

    const [correo, setCorreo] = useState("");
    const [contrasena, setContrasena] = useState("");

    const navigate = useNavigate();

    function iniciarSesion() {

        if (correo === "") {
            alert("Ingrese su correo electrónico.");
            return;
        }

        if (contrasena === "") {
            alert("Ingrese su contrasena.");
            return;
        }

        navigate("/inicio");
    }

    return (
        <div className="login-container">

            <div className="login-card">

                {/* LOGO */}

                <div className="login-logo">

                    <div className="login-logo-icon">

                    </div>

                    <span>
                        LUKELIAH
                    </span>

                </div>


                {/* DESCRIPCION */}

                <p className="login-descripcion">
                    Sistema Web de Gestión para
                    <br />
                    Emprendimientos de Postres
                </p>


                {/* FORMULARIO */}

                <div className="login-form">


                    {/* CORREO */}

                    <div className="mb-3">

                        <label className="form-label">
                            Correo electrónico
                        </label>

                        <input
                            type="email"
                            className="form-control"
                            placeholder="correo@ejemplo.com"
                            value={correo}
                            onChange={(e) =>
                                setCorreo(e.target.value)
                            }
                        />

                    </div>


                    {/* CONTRASENA */}

                    <div className="mb-3">

                        <label className="form-label">
                            Contrasena
                        </label>

                        <input
                            type="password"
                            className="form-control"
                            placeholder="••••••••"
                            value={contrasena}
                            onChange={(e) =>
                                setContrasena(e.target.value)
                            }
                        />

                    </div>


                    {/* BOTON */}

                    <button
                        type="button"
                        className="btn login-btn"
                        onClick={iniciarSesion}
                    >
                        Iniciar sesión
                    </button>

                </div>


                {/* VERSION */}

                <div className="login-version">
                    LUKELIAH v1.0
                </div>

            </div>

        </div>
    );
}

export default Login;