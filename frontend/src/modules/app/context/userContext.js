import React, { useState, useEffect } from "react";
import { getUser } from "modules/login/adapter";
import { TokenContext } from "modules/app/context/TokenContext.js";
import { Redirect } from "react-router-dom";


export const UserContext = React.createContext();

const UserProvider = ({ children }) => {
    const { token, setToken, deleteToken } = React.useContext(TokenContext);
    const [user, setUser] = useState(null);
    const [loggedIn, setLoggedIn] = useState(false);

    const _getUser = (token) => {
        getUser(token.access).then(user => {
            setUser(user);
        })
        .catch(error => {
            console.log("Failed to log in");
            deleteToken();
        });
    };

    const updateToken = newToken => {
        setToken(newToken);
    };

    const refreshUserData = () => {
        _getUser(token);
    };

    // the log in process sets the state in this order:
    // token -> user -> loggedIn
    // the log out process sets the state in this order:
    // token -> loggedIn -> user
    useEffect(() => {
        // log in
        if (token !== null) {
            _getUser(token);
        }
        // log out
        else {
            setLoggedIn(false);
        }
    }, [token]);

    // log in when user object is set
    useEffect(() => {
        if (user !== null) {
            setLoggedIn(true);
        }
    }, [user]);

    // remove user when we log out
    useEffect(() => {
        if (!loggedIn) {
            setUser(null);
        }
    }, [loggedIn]);


    return (
        <>
            {loggedIn && <Redirect to="/login" />}
            <UserContext.Provider value={{ user, loggedIn, token, updateToken, refreshUserData }}>
                {children}
            </UserContext.Provider>
        </>
    );
};

export default UserProvider;
