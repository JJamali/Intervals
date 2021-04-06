import LoginForm from "./components/LoginForm.js";
import React from "react";
import { Link } from "react-router-dom";

export default function Login() {
    return (
        <>
            <h2>Login Page</h2>
            <LoginForm />
            <Link to="/signup">Sign up</Link>
        </>
    )
}
