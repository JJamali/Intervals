import React, { useState } from "react";
import { getUser } from "modules/login/adapter";

export const UserContext = React.createContext();

const UserProvider = ({ children }) => {
    const [token, setToken] = useState({access: "", refresh: ""});
    const [user, setUser] = useState({access: "", refresh: ""});
    const [loggedIn, setLoggedIn] = useState(false);

    const updateToken = token => {
        setToken(token);
        loginUser(token.access);
    };

    const loginUser = access => {
        getUser(access).then(user => {
            setUser(user);
            setLoggedIn(true);
            console.log("current user:", user);
        });
    };

    const refreshUserData = () => {
        loginUser(token.access);
    }

    return (
        <UserContext.Provider value={{ user, loggedIn, token, updateToken, refreshUserData }}>
            {children}
        </UserContext.Provider>
    );
};

export default UserProvider;
