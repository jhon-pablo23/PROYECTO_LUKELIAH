import { useState, useEffect } from "react";
import {
  BrowserRouter,
  Routes,
  Route,
  Navigate,
  useLocation
} from "react-router-dom";

import Login from "./components/login/login";
import Menu from "./components/menu/menu";
import Panel from "./components/panel/panel";
import Usuarios from "./components/usuarios/usuarios";
import Ingredientes from "./components/ingredientes/ingredientes";
import Recetas from "./components/recetas/recetas";
import Postres from "./components/postres/postres";
import Ventas from "./components/ventas/ventas";
import Catalogo from "./components/catalogo/catalogo";


function Aplicacion() {

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


  const location = useLocation();

  const esLogin = location.pathname === "/login";


  return (

    <div className="min-vh-100">

      {/* ENCABEZADO SUPERIOR */}

      {!esLogin && (

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

      )}


      {/* MENU + CONTENIDO */}

      <div className={esLogin ? "" : "d-flex"}>

        {/* MENU */}

        {!esLogin && <Menu />}


        {/* CONTENIDO */}

        <main
          className={esLogin ? "" : "flex-grow-1 p-4"}
        >

          <Routes>

            {/* PAGINA INICIAL */}

            <Route
              path="/"
              element={<Navigate to="/login" />}
            />


            {/* LOGIN */}

            <Route
              path="/login"
              element={<Login />}
            />


            {/* DASHBOARD */}

            <Route
              path="/inicio"
              element={<Panel />}
            />


            {/* USUARIOS */}

            <Route
              path="/usuarios"
              element={<Usuarios />}
            />


            {/* INGREDIENTES */}

            <Route
              path="/ingredientes"
              element={<Ingredientes />}
            />


            {/* RECETAS */}

            <Route
              path="/recetas"
              element={<Recetas />}
            />


            {/* POSTRES */}

            <Route
              path="/postres"
              element={<Postres />}
            />


            {/* VENTAS */}

            <Route
              path="/ventas"
              element={<Ventas />}
            />


            {/* CATALOGO PUBLICO */}

            <Route
              path="/catalogo"
              element={<Catalogo />}
            />

          </Routes>

        </main>

      </div>

    </div>

  );
}


function App() {

  return (

    <BrowserRouter>

      <Aplicacion />

    </BrowserRouter>

  );
}


export default App;