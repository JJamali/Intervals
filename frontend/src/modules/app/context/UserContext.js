import React, { useState, useEffect } from "react";
import { getUser, logout } from "./adapter";
import { Redirect } from "react-router-dom";


export const UserContext = React.createContext();

const UserProvider = ({ children }) => {

    const [user, setUser] = useState(null);
    const [loggedIn, setLoggedIn] = useState(false);

    const _getUser = () => {
        getUser().then(response => {
            const user = response.data;
            console.log("Logged in", user);
            setUser(user);
        })
        .catch(error => {
            console.log("Failed to log in");
            setLoggedIn(false);
        });
    };

    const refreshUserData = () => {
        _getUser();
    };

    const logoutUser = () => {
        logout();
        setLoggedIn(false);
    }

    // the log in process sets the state in this order:
    // user -> loggedIn
    // the log out process sets the state in this order:
    // loggedIn -> user

    // log in when user object is set
    useEffect(() => {
        if (user !== null) {
            console.log(user.profile);
            setLoggedIn(true);
        }
    }, [user]);

    // remove user when we log out
    useEffect(() => {
        if (!loggedIn) {
            setUser(null);
        }
    }, [loggedIn]);

    // try to log in on load
    useEffect(() => {
        _getUser();
    }, []);


    return (
        <>
            {loggedIn && <Redirect to="/login" />}
            <UserContext.Provider value={{ user, loggedIn, refreshUserData, logout: logoutUser }}>
                {children}
            </UserContext.Provider>
        </>
    );
};

export default UserProvider;
