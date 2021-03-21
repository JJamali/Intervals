import LoginForm from './components/LoginForm.js';
import React from 'react';
import { Redirect } from 'react-router-dom';
import {UserContext} from './UserContext.js';

export default function Login({setToken}) {
    const loggedIn = (user) => {
        // if the user object is empty they are not logged in
        // method taken from https://stackoverflow.com/a/32108184
        const isEmpty = user &&
            Object.keys(user).length === 0 && user.constructor === Object;

        return !isEmpty;
    }

    function handle_login(e, data) {
        e.preventDefault();
        fetch('http://localhost:8000/api/token/', { // Handle login
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(res => res.json())
        .then(json => {
            setToken(json);
        })
        .catch(error => {
            console.error('Unable to login:', error);
        });
    }

    return (
        <UserContext.Consumer>
            {({user, setUser}) => (
                <>
                    <h2>Login Page</h2>
                    <LoginForm handle_login={handle_login} />
                    {loggedIn(user) && <Redirect to='/' />}
                </>
            )}
        </UserContext.Consumer>
    )
}
