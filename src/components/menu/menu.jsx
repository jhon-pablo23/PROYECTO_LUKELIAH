import { Link } from "react-router-dom";

function Menu() {
    return (
        <div
            className="d-flex flex-column text-white p-3 min-vh-100"
            style={{
                width: "240px",
                backgroundColor: "#1f426b"
            }}
        >

            <nav className="nav flex-column">

                <Link to="/inicio" className="nav-link text-white">
                    Dashboard
                </Link>

                <Link to="/usuarios" className="nav-link text-white">
                    Usuarios
                </Link>

                <Link to="/ingredientes" className="nav-link text-white">
                    Ingredientes
                </Link>

                <Link to="/recetas" className="nav-link text-white">
                    Recetas
                </Link>

                <a href="#" className="nav-link text-white">
                    Postres
                </a>

                <a href="#" className="nav-link text-white">
                    Ventas
                </a>

                <a href="#" className="nav-link text-white">
                    Catálogo Público
                </a>

            </nav>

        </div>
    );
}

export default Menu;