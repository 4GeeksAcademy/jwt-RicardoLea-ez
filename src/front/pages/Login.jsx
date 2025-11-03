import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import useGlobalReducer from "../hooks/useGlobalReducer";

export const Login = () => {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);

    const { dispatch } = useGlobalReducer();
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError("");

        try {
            const backendUrl = import.meta.env.VITE_BACKEND_URL;

            if (!backendUrl) {
                throw new Error("VITE_BACKEND_URL is not defined in .env file");
            }

            console.log("Enviando login a:", backendUrl + "/api/login");

            const response = await fetch(backendUrl + "/api/login", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    email: email,
                    password: password,
                }),
            });

            const data = await response.json();
            console.log("Respuesta del backend:", data);

            if (response.ok) {
                // Login exitoso, guardar token y redirigir
                dispatch({
                    type: "set_token",
                    payload: {
                        token: data.token,
                        user: data.user
                    }
                });
                navigate("/private");
            } else {
                setError(data.message || "Error en el inicio de sesión");
            }
        } catch (error) {
            console.error("Error completo:", error);
            setError("Error de conexión con el servidor: " + error.message);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="container mt-5">
            <div className="row justify-content-center">
                <div className="col-md-6">
                    <div className="card">
                        <div className="card-body">
                            <h2 className="card-title text-center mb-4">Iniciar Sesión</h2>

                            {error && (
                                <div className="alert alert-danger" role="alert">
                                    {error}
                                </div>
                            )}

                            <form onSubmit={handleSubmit}>
                                <div className="mb-3">
                                    <label htmlFor="email" className="form-label">
                                        Email
                                    </label>
                                    <input
                                        type="email"
                                        className="form-control"
                                        id="email"
                                        value={email}
                                        onChange={(e) => setEmail(e.target.value)}
                                        required
                                    />
                                </div>

                                <div className="mb-3">
                                    <label htmlFor="password" className="form-label">
                                        Contraseña
                                    </label>
                                    <input
                                        type="password"
                                        className="form-control"
                                        id="password"
                                        value={password}
                                        onChange={(e) => setPassword(e.target.value)}
                                        required
                                    />
                                </div>

                                <button
                                    type="submit"
                                    className="btn btn-primary w-100"
                                    disabled={loading}
                                >
                                    {loading ? "Iniciando sesión..." : "Iniciar Sesión"}
                                </button>
                            </form>

                            <div className="text-center mt-3">
                                <p>
                                    ¿No tienes cuenta? <Link to="/signup">Regístrate</Link>
                                </p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};