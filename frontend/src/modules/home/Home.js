import React from 'react';
import {
    Redirect
} from "react-router-dom";
import { Container } from "@material-ui/core";
import Profile from './Profile.js';
import Quiz from './quiz/Quiz.js';
import { UserContext } from "modules/app/context/UserContext.js";


export default function Home() {
    const { loggedIn } = React.useContext(UserContext);

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
