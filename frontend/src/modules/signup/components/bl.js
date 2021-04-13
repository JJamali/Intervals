import React, { useState } from "react";
import { UserContext } from "modules/app/context/UserContext.js";
import { signup } from "../adapter";


export default function SignupFormBl() {
    const { loggedIn, refreshUserData } = React.useContext(UserContext);
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [signupFailed, setSignupFailed] = useState(false);

    const handleSubmit = e => {
        signup(username, password).then(response => {
            // success
            setSignupFailed(false);
            refreshUserData();
        }).catch(error => {
            // couldn't sign up for some reason
            // probably caused by user already existing
            console.log("sign up error", error);
            setSignupFailed(true);
        });
        e.preventDefault();
    };

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
