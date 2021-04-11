import React, { useState } from "react";
import { refreshToken } from "api/token.js";


export const TokenContext = React.createContext();

const TokenProvider = (props) => {
    const getToken = () => {
        const tokenString = localStorage.getItem("token");
        const userToken = JSON.parse(tokenString);
        // const userToken = null;
        console.log("got token", userToken);
        return userToken;
    };
    const [token, setToken] = useState(getToken());


    const saveToken = userToken => {
        localStorage.setItem("token", JSON.stringify(userToken));
        setToken(userToken);
        console.log("Set", userToken);
        _silentRefresh(userToken.refresh);
    };


    const _silentRefresh = (refresh) => {
        // call refresh token endpoint
        console.log("REFRESHING...", refresh);
        refreshToken(refresh).then(response => {
            if (response !== null) {
                // success
                // store new token and restart cooldown
                const newAccess = response.access;
                setToken({ refresh: refresh, access: newAccess });
                setTimeout(() => _silentRefresh(refresh), 5*60*1000);
                // console.log("newAccess", newAccess);
                // console.log("token", token.access);
            }
            else {
                // on fail
                // redirect to login page
                console.log("Failed to refresh");
                // delete token, indicating that it's invalid
                deleteToken();
            }
        });
    };


    const deleteToken = () => {
        sessionStorage.removeItem("token");
        setToken(null);
    };


    return (
        <>
            <TokenContext.Provider value={{ token, setToken: saveToken, deleteToken }}>
                {props.children}
            </TokenContext.Provider>
        </>
    );
};

export default TokenProvider;
