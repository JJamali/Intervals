import React, {useState, useEffect} from "react";
import { UserContext } from "modules/app/context/userContext.js";
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

    return { username, password, loggedIn, handleChange, handleSubmit, loginFailed };
}
