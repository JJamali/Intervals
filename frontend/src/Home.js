import React, { Component, useState, useEffect } from 'react';
import {
    BrowserRouter as Router,
    Switch,
    Route,
    Redirect
} from "react-router-dom";
import Profile from './Profile.js';
import Quiz from './Quiz.js';
import { UserContext } from './UserContext.js';
import { TokenContext } from './TokenContext.js';


export default function Home() {
    const loggedIn = (user) => {
        console.log(user);
        // if the user object is empty they are not logged in
        // method taken from https://stackoverflow.com/a/32108184
        const isEmpty = user &&
            Object.keys(user).length === 0 && user.constructor === Object;

        return !isEmpty;
    }

    return (
        <UserContext.Consumer>
            {({user, updateUser}) => {
                if (!loggedIn(user)) {
                    return <Redirect to='/login' />;
                }
                else {
                    return (
                        <>
                            <Profile user={user} />
                            <TokenContext.Consumer>
                                {({token, setToken}) => (
                                    <Quiz token={token} updateUser={updateUser} />
                                )}
                            </TokenContext.Consumer>
                        </>
                    )
                }
            }}
        </UserContext.Consumer>
    );
}
