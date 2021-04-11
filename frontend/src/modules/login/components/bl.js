import React, { useState } from "react";
import { UserContext } from "modules/app/context/UserContext.js";
import { login } from "../adapter";


export default function LoginFormBl() {
    const { loggedIn, updateToken } = React.useContext(UserContext);
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [loginFailed, setLoginFailed] = useState(false);

    const handleSubmit = e => {
        login(username, password).then(response => {
            if (response === null) {
                // invalid login or another error
                setLoginFailed(true);
            }
            else {
                updateToken({refresh: response.refresh, access: response.access});
            }
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
