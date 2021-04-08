import React, { Component, useState, useEffect } from 'react';
import {
    BrowserRouter as Router,
    Switch,
    Route,
    Redirect
} from "react-router-dom";
import { Container } from "@material-ui/core";
import Profile from './Profile.js';
import Quiz from './quiz/Quiz.js';
import { UserContext } from "modules/app/context/userContext.js";


export default function Home() {
    const { loggedIn, refreshUserData } = React.useContext(UserContext);

    return (
        <Container>
            {!loggedIn ? <Redirect to="/login" /> :
            <UserContext.Consumer>
                {({ user, token }) =>
                    <>
                        <Profile user={user} />
                        <Quiz />
                    </>
                }
            </UserContext.Consumer>}
        </Container>
    );
}
