import React, { Component, useState, useEffect } from 'react';
import './App.css';
import {
    BrowserRouter as Router,
    Switch,
    Route,
    Redirect
} from "react-router-dom";
import Login from 'modules/login/Login.js';
import Signup from 'modules/signup/Signup.js';
import Home from 'modules/home/Home.js';
import UserProvider from "modules/app/context/userContext.js";

class App extends Component {
    constructor(props) {
        super(props);

        this.updateUser = () => {
            this.getUserWithToken();
        };

        this.state = {
            token: {},
            user: {},
            updateUser: this.updateUser,
        };
    }

    setToken = (token) => {
        this.setState({token: token});
    };

    componentDidUpdate(prevProps, prevState) {
        if (this.state.token !== prevState.token) {
            //this.getUserWithToken();
        }
    }

    render() {
        const value = {
            token: this.state.token,
            setToken: this.setToken
        }
        return (
            <UserProvider>
                <Router>
                    <Switch>
                        <Route exact path="/">
                            <Home />
                        </Route>
                        <Route path="/login">
                            <Login />
                        </Route>
                        <Route path="/signup">
                            <Signup setToken={this.setToken} />
                        </Route>
                    </Switch>
                </Router>
            </UserProvider>
        );
    }
}

export default App;
