import SignupForm from './components/SignupForm.js';
import React from 'react';
import { Link } from 'react-router-dom';


export default function Signup({setToken}) {
    return (
        <>
            <h2>Signup Page</h2>
            <SignupForm />
            <Link to="/login">Log in</Link>
        </>
    )
}
