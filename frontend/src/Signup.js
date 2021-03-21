import SignupForm from './components/SignupForm.js';
import React from 'react';
import { Redirect } from 'react-router-dom';
import {UserContext} from './UserContext.js';


export default function Signup({setToken}) {
    const loggedIn = (user) => {
        // if the user object is empty they are not logged in
        // method taken from https://stackoverflow.com/a/32108184
        const isEmpty = user &&
            Object.keys(user).length === 0 && user.constructor === Object;

        return !isEmpty;
    }

    function handle_signup(e, data) {
        e.preventDefault();
        fetch('http://localhost:8000/api/intervals/users/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(res => res.json())
        .then(json => {
            console.log(json);
            //this.setState({jwt_token: json.token}); // Sets token
            setToken(json.token);
            //update_user(json.user);
        });
    };

    return (
        <UserContext.Consumer>
            {({user, setUser}) => (
                <>
                    <h2>Signup Page</h2>
                    <SignupForm handle_signup={handle_signup} />
                    {loggedIn(user) && <Redirect to='/' />}
                </>
            )}
        </UserContext.Consumer>
    )
}
