import React from 'react';
import {
    Redirect
} from "react-router-dom";
import { Container } from "@material-ui/core";
import Profile from './Profile.js';
import Quiz from './quiz/Quiz.js';
import { UserContext } from "modules/app/context/UserContext.js";


export default function Home() {
    const { loggedIn, logout } = React.useContext(UserContext);

    if (!loggedIn) {
        return (<Redirect to="/login" />);
    }

    return (
        <Container>
            <UserContext.Consumer>
                {({ user, token }) =>
                    <>
                        <Profile user={user} />
                        <Quiz />
                    </>
                }
            </UserContext.Consumer>
            <button type="button" onClick={logout}>
                Logout
            </button>
        </Container>
    );
}
