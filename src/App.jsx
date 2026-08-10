import { useState, useEffect } from "react";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";

import Menu from "./components/menu/menu";
import Panel from "./components/panel/panel";
import Usuarios from "./components/usuarios/usuarios";
import Ingredientes from "./components/ingredientes/ingredientes";

function App() {

  const [hora, setHora] = useState("");

  useEffect(() => {

    function actualizarHora() {
      const ahora = new Date();

      setHora(
        ahora.toLocaleTimeString("es-PE", {
          hour: "2-digit",
          minute: "2-digit",
          second: "2-digit"
        })
      );
    }

    actualizarHora();

    const intervalo = setInterval(actualizarHora, 1000);

    return () => clearInterval(intervalo);

  }, []);


  return (
    <BrowserRouter>

      <div className="min-vh-100">

        {/* ENCABEZADO SUPERIOR */}

        <header
          className="d-flex justify-content-between align-items-center px-4"
          style={{
            height: "70px",
            backgroundColor: "#ffffff",
            borderBottom: "1px solid #e5e5e5"
          }}
        >

          {/* LOGO */}

          <div>
            <h4
              className="mb-0 fw-bold"
              style={{
                color: "#1f426b"
              }}
            >
              LUKELIAH
            </h4>
          </div>


          {/* INFORMACION DEL USUARIO */}

          <div className="d-flex align-items-center">

            {/* CIRCULO DEL USUARIO */}

            <div
              className="d-flex justify-content-center align-items-center me-3"
              style={{
                width: "40px",
                height: "40px",
                borderRadius: "50%",
                backgroundColor: "#1f426b",
                color: "white",
                fontWeight: "bold"
              }}
            >
              J
            </div>


            {/* NOMBRE Y ROL */}

            <div className="me-4">

              <div
                style={{
                  fontSize: "14px",
                  fontWeight: "700"
                }}
              >
                JHON EMERSON ANCHAYHUA PABLO
              </div>

              <div
                style={{
                  fontSize: "12px",
                  color: "#777"
                }}
              >
                admin
              </div>

            </div>


            {/* HORA */}

            <div
              className="me-4"
              style={{
                fontSize: "14px",
                fontWeight: "600",
                color: "#1f426b"
              }}
            >
              {hora}
            </div>


            {/* CERRAR SESION */}

            <button
              type="button"
              className="btn btn-link text-dark text-decoration-none"
              onClick={() =>
                alert("Sesion cerrada")
              }
            >
              Cerrar sesión
            </button>

          </div>

        </header>


        {/* MENU + CONTENIDO */}

        <div className="d-flex">

          <Menu />

          <main className="flex-grow-1 p-4">

            <Routes>

              <Route
                path="/"
                element={<Navigate to="/inicio" />}
              />

              <Route
                path="/inicio"
                element={<Panel />}
              />

              <Route
                path="/usuarios"
                element={<Usuarios />}
              />

              <Route
                path="/ingredientes"
                element={<Ingredientes />}
              />

            </Routes>

          </main>

        </div>

      </div>

    </BrowserRouter>
  );
}

export default App;