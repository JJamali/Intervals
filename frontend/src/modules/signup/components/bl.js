import React, { useState } from "react";
import { UserContext } from "modules/app/context/UserContext.js";
import { signup } from "../adapter";


export default function SignupFormBl() {
    const { loggedIn, updateToken } = React.useContext(UserContext);
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [signupFailed, setSignupFailed] = useState(false);

    const handleSubmit = e => {
        signup(username, password).then(response => {
            if (response === null) {
                // user already exists or some other error
                setSignupFailed(true);
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

    return { username, password, loggedIn, handleChange, handleSubmit, signupFailed };
}
