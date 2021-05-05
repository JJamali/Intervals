import React, { useState } from "react";
import { UserContext } from "modules/app/context/UserContext.js";
import { login } from "../adapter";


export default function LoginFormBl() {
    const { getUserId, loggedIn } = React.useContext(UserContext);
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [loginFailed, setLoginFailed] = useState(false);

    const handleSubmit = e => {
        login(username, password).then(response => {
            console.log('status', response.status)
            // good to log in
            console.log(response);
            setLoginFailed(false);
            getUserId();
        }).catch(error => {
            // not good to log in :(
            console.log('error', error);
            setLoginFailed(true);
        });
        e.preventDefault();
    }

    const handleChange = e => {
        const name = e.target.name;
        const value = e.target.value;

        if (name === "username") {
            setUsername(value);
        }
        else {
            setPassword(value);
        }
    };

    return { loggedIn, handleChange, handleSubmit, loginFailed };
}
