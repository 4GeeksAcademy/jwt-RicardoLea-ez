import { Link } from "react-router-dom";
import useGlobalReducer from "../hooks/useGlobalReducer";

export const Navbar = () => {
	const { store, dispatch } = useGlobalReducer();

	const handleLogout = () => {
		dispatch({ type: "logout" });
	};

	return (
		<nav className="navbar navbar-light bg-light">
			<div className="container">
				<Link to="/">
					<span className="navbar-brand mb-0 h1">React Boilerplate</span>
				</Link>
				<div className="ml-auto d-flex align-items-center">
					{store.token ? (
						<>
							<span className="navbar-text me-3">
								Bienvenido, {store.user?.email}
							</span>
							<Link to="/private" className="btn btn-outline-primary me-2">
								Área Privada
							</Link>
							<button
								className="btn btn-outline-danger"
								onClick={handleLogout}
							>
								Cerrar Sesión
							</button>
						</>
					) : (
						<>
							<Link to="/login" className="btn btn-outline-primary me-2">
								Iniciar Sesión
							</Link>
							<Link to="/signup" className="btn btn-primary">
								Registrarse
							</Link>
						</>
					)}
				</div>
			</div>
		</nav>
	);
};