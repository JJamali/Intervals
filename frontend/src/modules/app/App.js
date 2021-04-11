import React, { Component } from "react";
import "./App.css";
import {
    BrowserRouter as Router,
    Switch,
    Route
} from "react-router-dom";
import Grid from "@material-ui/core/grid";
import Login from "modules/login/Login.js";
import Signup from "modules/signup/Signup.js";
import Home from "modules/home/Home.js";
import UserProvider from "modules/app/context/UserContext.js";
import TokenProvider from "modules/app/context/TokenContext.js";

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
        return (
            <Grid container justify="center">
                <Grid item>
                    <Router>
                        <TokenProvider>
                            <UserProvider>
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
                            </UserProvider>
                        </TokenProvider>
                    </Router>
                </Grid>
            </Grid>
        );
    }
}

export default App;
