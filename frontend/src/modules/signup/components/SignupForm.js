import React from "react";
import { Redirect } from 'react-router-dom';
import SignupFormBl from "./bl.js";

export default function SignupForm() {
    const { username, password, loggedIn, handleChange, handleSubmit, signupFailed } = SignupFormBl();

    return (
        <>
            {loggedIn ? <Redirect to="/" /> :
            <form onSubmit={handleSubmit}>
                <h4>Sign up In</h4>
                <label>
                    Username:
                    <input type="text" name="username" value={username} onChange={handleChange} />
                </label>
                <label>
                    Password:
                    <input type="password" name="password" value={password} onChange={handleChange} />
                </label>
                <input type="submit" value="Submit" />
                {signupFailed && <p>That username is already in use</p>}
            </form>}
        </>
    );
}
