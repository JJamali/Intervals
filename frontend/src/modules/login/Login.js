import LoginForm from "./components/LoginForm.js";
import React from "react";
import { Grid } from "@material-ui/core";
import { Link } from "react-router-dom";

export default function Login() {
    return (
        <Grid style={{textAlign: "center"}}>
            <h2>Login Page</h2>
            <LoginForm />
            <Link to="/signup">Sign up</Link>
        </Grid>
    )
}
