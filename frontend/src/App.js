import React, { Component, useState, useEffect } from 'react';
import Nav from './components/Nav';
import SignupForm from './components/SignupForm';
import './App.css';
import {
    BrowserRouter as Router,
    Switch,
    Route,
    Redirect
} from "react-router-dom";
import Login from './Login.js';
import Signup from './Signup.js';
import Home from './Home.js';
import { UserContext } from './UserContext.js';
import { TokenContext } from './TokenContext.js';

class App extends Component {
    constructor(props) {
        super(props);

        this.setToken = (token) => {
            this.setState({token: token});
        };
        this.updateUser = () => {
            this.getUserWithToken();
        };

        this.state = {
            token: {},
            user: {},
            updateUser: this.updateUser,
        };
    }

    // get user data from backend
    getUserWithToken = () => {
        if (this.state.token.access === undefined) {
            throw new Error();
        }
        fetch('http://localhost:8000/api/intervals/current_user/', {
            headers: {
                Authorization: `Bearer ${this.state.token.access}`
            }
        })
        .then(res => {
            if (!res.ok) {
                console.error('not logged in');
                return;
            }
            return res.json()
        })
        .then(user => {
            console.log('user', user);
            this.setState({user: user});
        });
    };

    componentDidUpdate(prevProps, prevState) {
        if (this.state.token !== prevState.token) {
            this.getUserWithToken();
        }
    }

    render() {

        return (
            <TokenContext.Provider value={{token: this.state.token, setToken: this.state.setToken}}>
            <UserContext.Provider value={{user: this.state.user, updateUser: this.state.updateUser}}>
                <Router>
                    <Switch>
                        <Route exact path="/">
                            <Home />
                        </Route>
                        <Route path="/login">
                            <Login setToken={this.setToken} />
                        </Route>
                        <Route path="/signup">
                            <Signup setToken={this.setToken} />
                        </Route>
                    </Switch>
                </Router>
            </UserContext.Provider>
            </TokenContext.Provider>
        );
    }
}

export default App;
