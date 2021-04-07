import LoginForm from "./components/LoginForm.js";
import React from "react";
import { Link, Grid } from "@material-ui/core";

export default function Login() {
    return (
        <Grid style={{textAlign: "center"}}>
            <h2>Login Page</h2>
            <LoginForm />
            <Link href="/signup">Sign up</Link>
        </Grid>
    )
}
