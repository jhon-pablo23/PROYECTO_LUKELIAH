import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";

import Menu from "./components/menu/menu";
import Panel from "./components/panel/panel";
import Usuarios from "./components/usuarios/usuarios";

function App() {
  return (
    <BrowserRouter>

      <div className="d-flex min-vh-100">

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

          </Routes>

        </main>

      </div>

    </BrowserRouter>
  );
}

export default App;