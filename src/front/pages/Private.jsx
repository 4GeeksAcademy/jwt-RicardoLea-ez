import React, { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import useGlobalReducer from "../hooks/useGlobalReducer";

export const Private = () => {
    const { store, dispatch } = useGlobalReducer();
    const navigate = useNavigate();

    useEffect(() => {
        // Verificar si el usuario está autenticado
        if (!store.token) {
            navigate("/login");
        }
    }, [store.token, navigate]);

    const handleLogout = () => {
        dispatch({ type: "logout" });
        navigate("/login");
    };

    // Si no hay token, no renderizar nada (será redirigido por el useEffect)
    if (!store.token) {
        return null;
    }

    return (
        <div className="container mt-5">
            <div className="row justify-content-center">
                <div className="col-md-8">
                    <div className="card">
                        <div className="card-body text-center">
                            <h1 className="display-4">¡Bienvenido!</h1>
                            <p className="lead">
                                Esta es una página privada. Solo usuarios autenticados pueden ver este contenido.
                            </p>

                            {store.user && (
                                <div className="alert alert-info">
                                    <strong>Usuario:</strong> {store.user.email}
                                </div>
                            )}

                            <button
                                className="btn btn-danger mt-3"
                                onClick={handleLogout}
                            >
                                Cerrar Sesión
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};