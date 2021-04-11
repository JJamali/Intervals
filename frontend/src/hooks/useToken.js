import { useState } from "react";
import { refreshToken } from "api/token.js";

export default function useToken() {
    const getToken = () => {
        const tokenString = sessionStorage.getItem("token");
        const userToken = JSON.parse(tokenString);
        return userToken;
    };

    const [token, setToken] = useState(getToken());

    const saveToken = userToken => {
        sessionStorage.setItem("token", JSON.stringify(userToken));
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
                setTimeout(() => _silentRefresh(refresh), 10*1000);
                // console.log("newAccess", newAccess);
                // console.log("token", token.access);
            }
            else {
                // on fail
                // redirect to login page
                console.log("Failed to refresh");
                window.location.replace("/login");
            }
        });
    };

    return {
        token,
        setToken: saveToken,
    };
}
