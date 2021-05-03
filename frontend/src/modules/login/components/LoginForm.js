import React from "react";
import { Redirect } from 'react-router-dom';
import { TextField, Button } from "@material-ui/core";
import LoginFormBl from "./bl.js";

export default function LoginForm() {
    const { loggedIn, handleChange, handleSubmit, loginFailed } = LoginFormBl();

    return (
        <>
            {loggedIn ? <Redirect to="/" /> :
            <form onSubmit={handleSubmit}>
                <div>
                    <TextField type="text" name="username" label="Username" onChange={handleChange} />
                </div>
                <div>
                    <TextField type="password" name="password" label="Password" onChange={handleChange} />
                </div>
                <Button type="submit">Submit</Button>
                {loginFailed && <p>Invalid login</p>}
            </form>}
        </>
    );
}
